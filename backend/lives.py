import asyncio
import logging
import json
from typing import Annotated, Optional

from livekit import agents, rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
    multimodal,
)
from livekit.plugins import google
from livekit.rtc import Track, TrackKind, VideoStream
from livekit.agents.voice_assistant import VoiceAssistant
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("live")
logger.setLevel(logging.INFO)

SPEAKING_FRAME_RATE = 1.0  # frames per second when speaking
NOT_SPEAKING_FRAME_RATE = 0.5  # frames per second when not speaking
JPEG_QUALITY = 80

SYSTEM_PROMPT = """
You are Ira, an Interviewer. You have joined a call with a candidate.
You need to ask 5 questions to evaluate the candidate. Make sure the questions are relevant to the role and the candidate's experience.
Be concise and short with your talk. Ask these Questions in the order they are given. Do not call out Q1, Q2, Q3, Q4, Q5 in your response.

Q1:Introduce yourself ?
Q2:Ask the Candidate about their projects & experience in the field.
Q3:Ask the Candidate about their technical skills. and Ask one Question in any one of those skills.
Q4:Ask the Candidate to solve a coding question and ask them to share their screen, open any editor and ask to write the code for it, wait until the candidate completes writing code.
Q5:Ask the Candidate to explain the code they wrote. If they didnt write the code, Tell the Candidate to Improve on it.

Finally wait for 10 seconds, give the Candidate an detailed evaluation of their performance with communication skills, technical skills, & problem-solving skills. 

Do not let the Candidate drag the Interview too long. Complete the Interview within 5 minutes. Do not Rush the Interview.

"""

class VisionAssistant:
    def __init__(self):
        self.agent: Optional[multimodal.MultimodalAgent] = None
        self.model: Optional[google.beta.realtime.RealtimeModel] = None
        self._is_user_speaking: bool = False

    async def start(self, ctx: JobContext):
        """Initialize and start the vision assistant."""
        await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
        participant = await ctx.wait_for_participant()

        chat_ctx = llm.ChatContext()
        self.model = google.beta.realtime.RealtimeModel(
            voice="Puck",
            temperature=0.8,
            instructions=SYSTEM_PROMPT,
        )

        self.agent = multimodal.MultimodalAgent(
            model=self.model,
            chat_ctx=chat_ctx,
        )
        self.agent.start(ctx.room, participant)

        # Add event handlers for user speaking state
        self.agent.on("user_started_speaking", self._on_user_started_speaking)
        self.agent.on("user_stopped_speaking", self._on_user_stopped_speaking)

        ctx.room.on(
            "track_subscribed",
            lambda track, pub, participant: asyncio.create_task(
                self._handle_video_track(track)
            )
            if track.kind == TrackKind.KIND_VIDEO
            else None,
        )

    async def _handle_video_track(self, track: Track):
        """Handle incoming video track and send frames to the model."""
        logger.info("Handling video track")
        video_stream = VideoStream(track)
        last_frame_time = 0
        frame_counter = 0

        async for event in video_stream:
            current_time = asyncio.get_event_loop().time()

            if current_time - last_frame_time < self._get_frame_interval():
                continue

            last_frame_time = current_time
            frame = event.frame

            frame_counter += 1

            try:
                self.model.sessions[0].push_video(frame)
                logger.info(f"Queued frame {frame_counter}")
            except Exception as e:
                logger.error(f"Error queuing frame {frame_counter}: {e}")

        await video_stream.aclose()

    def _get_frame_interval(self) -> float:
        """Get the interval between frames based on speaking state."""
        return 1.0 / (
            SPEAKING_FRAME_RATE if self._is_user_speaking else NOT_SPEAKING_FRAME_RATE
        )

    def _on_user_started_speaking(self):
        """Handler for when user starts speaking."""
        self._is_user_speaking = True
        logger.debug("User started speaking")

    def _on_user_stopped_speaking(self):
        """Handler for when user stops speaking."""
        self._is_user_speaking = False
        logger.debug("User stopped speaking")

async def entrypoint(ctx: JobContext):
    assistant = VisionAssistant()
    await assistant.start(ctx)

    async def write_transcript():
        filename = f"/tmp/transcript_{ctx.room.name}.json"
        with open(filename, 'w') as f:
            json.dump(agent.history.to_dict(), f, indent=2)

    ctx.add_shutdown_callback(write_transcript)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
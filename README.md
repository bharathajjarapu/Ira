# Ira

An AI Interview Assistant built with Next.js 14 and LiveKit for real-time voice conversations.

## Overview

Ira is a comprehensive interview assistance platform featuring:
- **Frontend**: Next.js 14 with LiveKit components for real-time audio/video
- **Backend**: Python-based LiveKit agent with Google AI integration
- **Voice Assistant**: Real-time conversational AI for interview practice

## Prerequisites

Before setting up Ira, ensure you have:

- **Node.js** (v18 or higher)
- **Python** (v3.9 or higher)
- **LiveKit** account and server access
- **Google Cloud** account with API access
- **Git** for version control

## Environment Variables

Create `.env.local` files in both frontend and backend directories with the following variables:

### Frontend (.env.local)
```env
NEXT_PUBLIC_LIVEKIT_URL=wss://your-livekit-server.com
```

### Backend (.env)
```env
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret
LIVEKIT_HOST=your-livekit-server.com
GOOGLE_API_KEY=your-google-api-key
```

## Project Structure

```
Ira/
├── frontend/           # Next.js 14 application
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── hooks/      # Custom React hooks
│   │   ├── pages/      # Next.js pages
│   │   └── styles/     # CSS styles
│   ├── package.json
│   └── .env.local      # Frontend environment variables
├── backend/            # Python LiveKit agent
│   ├── agent.py        # Main agent file
│   ├── requirements.txt
│   └── .env           # Backend environment variables
├── LICENSE
└── README.md
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/bharathajjarapu/Ira.git
cd Ira
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

Create `.env.local` with your LiveKit URL:
```env
NEXT_PUBLIC_LIVEKIT_URL=wss://your-livekit-server.com
```

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` with your credentials:
```env
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret
LIVEKIT_HOST=your-livekit-server.com
GOOGLE_API_KEY=your-google-api-key
```

## Running the Application

### 1. Start the Backend Agent

From the `backend` directory:

```bash
# Option 1: Direct execution
python agent.py

# Option 2: Using LiveKit agents worker
livekit agents worker
```

### 2. Start the Frontend

From the `frontend` directory:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

## Connection Methods

### Environment Variable Connection
- Set `NEXT_PUBLIC_LIVEKIT_URL` in frontend `.env.local`
- Application will auto-connect using the environment URL

### Token-based Connection
- Generate a LiveKit token with appropriate permissions
- Use the token to connect via the application interface

## Docker Support (Optional)

For containerized deployment:

### Frontend Dockerfile
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]
```

### Backend Dockerfile
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "agent.py"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_LIVEKIT_URL=${LIVEKIT_URL}
  
  backend:
    build: ./backend
    environment:
      - LIVEKIT_API_KEY=${LIVEKIT_API_KEY}
      - LIVEKIT_API_SECRET=${LIVEKIT_API_SECRET}
      - LIVEKIT_HOST=${LIVEKIT_HOST}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
```

## Troubleshooting

### Common Issues

**Connection Issues**
- Verify LiveKit server URL format: `wss://your-server.com`
- Check that API keys are correctly set in environment variables
- Ensure LiveKit server is accessible from your network

**Agent Not Starting**
- Verify Python dependencies are installed: `pip install -r requirements.txt`
- Check that Google API key has necessary permissions
- Ensure LiveKit credentials are valid

**Frontend Build Issues**
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version compatibility (v18+)

**Audio/Video Issues**
- Ensure browser permissions for microphone/camera access
- Check LiveKit room configuration and permissions
- Verify network connectivity for WebRTC

### Debug Mode

Enable debug logging:

**Frontend:**
```env
NEXT_PUBLIC_DEBUG=true
```

**Backend:**
```bash
export LIVEKIT_LOG_LEVEL=debug
python agent.py
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Create an issue in this repository
- Check the troubleshooting section above
- Review LiveKit documentation: https://docs.livekit.io/

---

**Built with ❤️ using Next.js 14, LiveKit, and Google AI**

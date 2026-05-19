---
title: AI Video Assistant
emoji: 🎥
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 8501
---

# AI Video Assistant

AI-powered meeting intelligence system for transcription, summarization, and RAG-based Q&A.

## Features

- **Video/Audio Processing**: Extract audio from YouTube URLs or local files
- **Transcription**: Convert speech to text using Faster-Whisper
- **Summarization**: Generate concise summaries with AI
- **RAG Chat**: Ask questions about your videos using vector search
- **Key Insights**: Extract action items, decisions, and questions

## Tech Stack

- **UI**: Streamlit
- **LLM**: Mistral AI
- **Vector Store**: ChromaDB
- **Transcription**: Faster-Whisper
- **Embeddings**: Sentence Transformers

## Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd AI-Video-Assistant--main-ver3
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your MISTRAL_API_KEY
```

5. Get your Mistral API key:
   - Visit [Mistral Console](https://console.mistral.ai/)
   - Create a free account
   - Generate an API key

6. Run the application:
```bash
python run.py
```

## Docker Deployment

### Build the Docker image
```bash
docker build -t ai-video-assistant .
```

### Run with Docker Compose
```bash
export MISTRAL_API_KEY=your_api_key_here
docker-compose up -d
```

### Recommended Production-Shaped Free Deployment

For the first public release, use an always-on VM and Docker:

1. Create an Oracle Cloud Always Free VM.
2. Install Docker and Docker Compose.
3. Clone this repo on the VM.
4. Add a `.env` file with `MISTRAL_API_KEY` and any optional overrides.
5. Set `CACHE_DIR`, `DOWNLOADS_DIR`, and `HF_HOME` to persistent paths if you mount a data volume.
6. Run `docker compose up -d --build`.
7. Put Caddy or Nginx in front of the app for HTTPS.

This keeps long transcription jobs on a machine that stays alive, which is a better fit than a sleeping free web host.

## Cloud Deployment

### Option 1: Hugging Face Spaces (Recommended)

1. Push your code to GitHub
2. Create account at [huggingface.co](https://huggingface.co)
3. Create new Space → Select "Docker" as SDK
4. Connect your GitHub repository
5. Add secret: `MISTRAL_API_KEY`

### Option 2: Render

1. Push your code to GitHub
2. Sign up at [render.com](https://render.com)
3. Create Web Service, connect GitHub
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `streamlit run app/main.py --server.address 0.0.0.0`
6. Add Environment Variable: `MISTRAL_API_KEY`

### Option 3: Railway

1. Push your code to GitHub
2. Sign up at [railway.app](https://railway.app)
3. Create project from GitHub
4. Add Environment Variable: `MISTRAL_API_KEY`

## Environment Variables

| Variable | Description |
|----------|-------------|
| `MISTRAL_API_KEY` | Required. Get from [Mistral Console](https://console.mistral.ai/) |
| `CACHE_DIR` | Optional. Directory for transcript and Chroma cache files |
| `DOWNLOADS_DIR` | Optional. Directory for downloaded or uploaded media |
| `HF_HOME` | Optional. Hugging Face cache directory |

## Project Structure

```
├── app/
│   ├── main.py          # Streamlit UI
│   └── ui/              # UI components
├── src/
│   ├── audio/           # Audio processing
│   ├── processing/      # LLM processing
│   ├── storage/        # Vector storage
│   └── transcription/  # Whisper transcription
├── Dockerfile           # Docker configuration
├── docker-compose.yml  # Docker Compose
└── requirements.txt    # Python dependencies
```

## License

MIT License

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

## Cloud Deployment

### Option 1: Hugging Face Spaces (Recommended)

1. Push your code to GitHub
2. Create account at [huggingface.co](https://huggingface.co)
3. Create new Space → Select "Streamlit" as SDK
4. Connect your GitHub repository
5. Add secrets: `MISTRAL_API_KEY`

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
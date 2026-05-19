FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    HF_HOME=/app/hf_cache \
    TRANSFORMERS_CACHE=/app/hf_cache \
    CACHE_DIR=/app/cache \
    DOWNLOADS_DIR=/app/downloads

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p cache downloads hf_cache

ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.address", "0.0.0.0"]

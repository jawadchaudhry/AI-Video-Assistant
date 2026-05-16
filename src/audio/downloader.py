"""YouTube audio downloader with yt-dlp."""

import logging
from pathlib import Path

import yt_dlp

from src.audio.paths import ensure_source_download_dir
from src.storage.cache import generate_source_id

logger = logging.getLogger(__name__)


def download_youtube_audio(url: str) -> Path:
    """
    Download audio from YouTube video.

    Args:
        url: YouTube video URL.

    Returns:
        Path to downloaded WAV file.

    Raises:
        yt_dlp.utils.DownloadError: If download fails.
    """
    source_id = generate_source_id(url)
    output_dir = ensure_source_download_dir(source_id)
    output_template = str(output_dir / f"{source_id}.%(ext)s")
    wav_path = output_dir / f"{source_id}.wav"

    if wav_path.exists():
        logger.info(f"Reusing existing YouTube audio: {wav_path}")
        return wav_path

    with yt_dlp.YoutubeDL({"quiet": True, "nocheckcertificate": True}) as info_ydl:
        info = info_ydl.extract_info(url, download=False)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "retries": 10,
        "fragment_retries": 10,
        "socket_timeout": 60,
        "nocheckcertificate": True,
        "quiet": False,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
    }

    logger.info(f"Downloading YouTube audio: {url}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = Path(ydl.prepare_filename(info))

    wav_path = file_path.with_suffix(".wav")
    logger.info(f"Audio downloaded to: {wav_path}")

    return wav_path

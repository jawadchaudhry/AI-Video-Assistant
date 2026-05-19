"""YouTube audio downloader with yt-dlp."""

import logging
import os
from pathlib import Path

import yt_dlp
from yt_dlp.utils import DownloadError

from src.audio.paths import ensure_source_download_dir
from src.storage.cache import generate_source_id

logger = logging.getLogger(__name__)


def _build_ydl_opts(output_template: str, player_clients: list[str] | None = None) -> dict:
    """Build yt-dlp options with resilient defaults for hosted environments."""
    ydl_opts: dict = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "retries": 10,
        "fragment_retries": 10,
        "extractor_retries": 5,
        "socket_timeout": 120,
        "nocheckcertificate": True,
        "quiet": False,
        "source_address": os.getenv("YTDLP_SOURCE_ADDRESS", "0.0.0.0"),
    }

    sleep_interval = os.getenv("YTDLP_SLEEP_INTERVAL")
    if sleep_interval:
        ydl_opts["sleep_interval"] = float(sleep_interval)

    max_sleep_interval = os.getenv("YTDLP_MAX_SLEEP_INTERVAL")
    if max_sleep_interval:
        ydl_opts["max_sleep_interval"] = float(max_sleep_interval)

    if player_clients:
        ydl_opts["extractor_args"] = {"youtube": {"player_client": player_clients}}

    return ydl_opts


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
    player_client_fallbacks = [
        None,
        ["web_embedded", "web"],
        ["android_embedded", "web"],
    ]

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

    last_error: Exception | None = None
    for player_clients in player_client_fallbacks:
        try:
            ydl_opts = _build_ydl_opts(output_template, player_clients)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = Path(ydl.prepare_filename(info))
                wav_path = file_path.with_suffix(".wav")
                if wav_path.exists():
                    logger.info("Audio downloaded to: %s", wav_path)
                    return wav_path
        except DownloadError as exc:
            last_error = exc
            logger.warning(
                "yt-dlp failed with player_clients=%s: %s",
                player_clients or "default",
                exc,
            )

    raise RuntimeError(
        "Failed to download YouTube audio after multiple yt-dlp attempts. "
        "The source may be temporarily unavailable or rate-limited."
    ) from last_error

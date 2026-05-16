"""Audio chunking for handling long audio files."""

import logging
import subprocess
from pathlib import Path
from typing import Optional

from src.audio.converter import convert_to_wav
from src.config import get_config

logger = logging.getLogger(__name__)


def chunk_audio(
    wav_path: str | Path,
    chunk_seconds: Optional[int] = None,
) -> list[Path]:
    """
    Split audio file into chunks of specified duration.

    Args:
        wav_path: Path to WAV audio file.
        chunk_seconds: Duration of each chunk. Defaults to config value.

    Returns:
        List of paths to chunked audio files.

    Raises:
        subprocess.CalledProcessError: If FFmpeg fails.
    """
    config = get_config()
    wav_path = Path(wav_path)
    chunk_seconds = chunk_seconds or config.audio_chunk_seconds

    output_pattern = str(wav_path.with_name(f"{wav_path.stem}_chunk_%03d.wav"))

    logger.info(f"Chunking audio into {chunk_seconds}s segments")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", str(wav_path),
            "-f", "segment",
            "-segment_time", str(chunk_seconds),
            "-c", "copy",
            output_pattern
        ],
        check=True,
        capture_output=True,
    )

    # Find all created chunks
    chunks = sorted(Path(wav_path.parent).glob(f"{wav_path.stem}_chunk_*.wav"))

    logger.info(f"Created {len(chunks)} audio chunks")
    return chunks


def process_input(source: str | Path) -> list[Path]:
    """
    Process any input source (YouTube URL or local file) to get audio chunks.

    Args:
        source: YouTube URL or local file path.

    Returns:
        List of paths to audio chunks ready for transcription.

    Raises:
        ValueError: If source is invalid.
        Exception: If processing fails.
    """
    from src.audio.downloader import download_youtube_audio

    source_str = str(source)

    if source_str.startswith("http"):
        logger.info("Processing YouTube source")
        wav_path = download_youtube_audio(source_str)
    else:
        logger.info("Processing local file")
        input_path = Path(source_str)
        if not input_path.exists():
            raise FileNotFoundError(f"Local file not found: {input_path}")
        wav_path = convert_to_wav(input_path)

    logger.info(f"Chunking audio: {wav_path}")
    chunks = chunk_audio(wav_path)

    return chunks

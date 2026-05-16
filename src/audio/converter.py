"""Audio file converter to standardize format."""

import logging
import subprocess
from pathlib import Path

from src.audio.paths import sanitize_name
from src.config import get_config

logger = logging.getLogger(__name__)


def convert_to_wav(input_path: str | Path, output_path: str | Path | None = None) -> Path:
    """
    Convert audio file to WAV format with standard settings.

    Args:
        input_path: Path to input audio file.
        output_path: Optional output path. If not provided, appends '_converted.wav'.

    Returns:
        Path to converted WAV file.

    Raises:
        subprocess.CalledProcessError: If FFmpeg fails.
    """
    config = get_config()
    input_path = Path(input_path)

    if output_path is None:
        output_path = input_path.with_name(f"{sanitize_name(input_path.stem)}.wav")
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Converting {input_path} to WAV format")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", str(input_path),
            "-ar", str(config.audio_sample_rate),
            "-ac", str(config.audio_channels),
            str(output_path)
        ],
        check=True,
        capture_output=True,
    )

    logger.info(f"Converted to: {output_path}")
    return output_path

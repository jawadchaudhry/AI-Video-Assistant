"""Whisper transcription using faster-whisper for efficient audio-to-text."""

import logging
from pathlib import Path
from typing import Optional

from faster_whisper import WhisperModel

from src.config import get_config

logger = logging.getLogger(__name__)

_model: Optional[WhisperModel] = None


def load_model() -> WhisperModel:
    """
    Load or return cached Whisper model.

    Returns:
        Loaded WhisperModel instance.
    """
    global _model

    config = get_config()

    if _model is None:
        logger.info(f"Loading faster-whisper model: {config.whisper_model}")
        _model = WhisperModel(
            config.whisper_model,
            device=config.whisper_device,
            compute_type=config.whisper_compute_type,
        )

    return _model


def transcribe_chunk(chunk_path: str | Path) -> str:
    """
    Transcribe a single audio chunk.

    Args:
        chunk_path: Path to audio chunk file.

    Returns:
        Transcribed text.
    """
    config = get_config()
    model = load_model()

    logger.debug(f"Transcribing: {chunk_path}")

    segments, _ = model.transcribe(
        str(chunk_path),
        beam_size=config.whisper_beam_size,
    )

    text = " ".join(seg.text for seg in segments).strip()
    return text


def transcribe_all(chunks: list[str | Path], language: str = "english") -> str:
    """
    Transcribe all audio chunks and combine results.

    Args:
        chunks: List of paths to audio chunk files.
        language: Language code for transcription.

    Returns:
        Combined transcribed text.
    """
    logger.info(f"Transcribing {len(chunks)} audio chunks")

    text_parts = []

    for i, chunk in enumerate(chunks):
        logger.info(f"Processing chunk {i+1}/{len(chunks)}")
        text_parts.append(transcribe_chunk(chunk))

    result = " ".join(text_parts).strip()
    logger.info(f"Transcription complete: {len(result)} characters")

    return result
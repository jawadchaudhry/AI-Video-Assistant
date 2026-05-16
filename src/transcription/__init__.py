"""Transcription module using Whisper for audio-to-text conversion."""

from src.transcription.whisper import load_model, transcribe_chunk, transcribe_all

__all__ = [
    "load_model",
    "transcribe_chunk",
    "transcribe_all",
]
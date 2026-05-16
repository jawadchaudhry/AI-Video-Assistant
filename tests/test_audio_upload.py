from __future__ import annotations

import hashlib
from pathlib import Path
from types import SimpleNamespace

import src.audio.converter as converter
import src.audio.uploader as uploader
from src.config import config as app_config


def test_save_uploaded_file_creates_unique_download_folder(tmp_path, monkeypatch):
    monkeypatch.setattr(app_config, "downloads_dir", tmp_path / "downloads", raising=False)

    payload = b"binary-video-data"
    expected_hash = hashlib.sha256(payload).hexdigest()[:12]

    uploaded_file = SimpleNamespace(
        name="Team Meeting.mp4",
        getbuffer=lambda: payload,
    )

    first_result = uploader.save_uploaded_file(uploaded_file)
    second_result = uploader.save_uploaded_file(uploaded_file)

    assert first_result.path.parent.name == f"local_{expected_hash}"
    assert first_result.path.name == f"local_{expected_hash}.mp4"
    assert first_result.path.read_bytes() == payload
    assert first_result.already_exists is False
    assert second_result.path == first_result.path
    assert second_result.already_exists is True


def test_convert_to_wav_writes_next_to_input_file(tmp_path, monkeypatch):
    input_file = tmp_path / "Local Clip.MP4"
    input_file.write_bytes(b"source-bytes")

    captured = {}

    def fake_run(cmd, check, capture_output):
        captured["cmd"] = cmd
        captured["check"] = check
        captured["capture_output"] = capture_output
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(
        converter,
        "get_config",
        lambda: SimpleNamespace(audio_sample_rate=16000, audio_channels=1),
    )
    monkeypatch.setattr(converter.subprocess, "run", fake_run)

    output_path = converter.convert_to_wav(input_file)

    assert output_path == input_file.with_name("Local_Clip.wav")
    assert captured["cmd"][0] == "ffmpeg"
    assert captured["cmd"][-1] == str(output_path)

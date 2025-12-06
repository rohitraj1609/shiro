import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# Base project directory (one level above this file, i.e. repo root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present at project root
load_dotenv(BASE_DIR / ".env")


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "voice_assistant")

    # Paths (resolved relative to project root)
    voice_input_dir: Path = (BASE_DIR / os.getenv("VOICE_INPUT_DIR", "voice/input_voice")).resolve()
    voice_output_dir: Path = (BASE_DIR / os.getenv("VOICE_OUTPUT_DIR", "voice/output_voice")).resolve()
    transcript_dir: Path = (BASE_DIR / os.getenv("TRANSCRIPT_DIR", "transcripts")).resolve()
    recorded_voice_dir: Path = (BASE_DIR / os.getenv("RECORDED_VOICE_DIR", "recorded_voice")).resolve()

    # Audio I/O
    sample_rate: int = int(os.getenv("SAMPLE_RATE", "16000"))
    channels: int = int(os.getenv("CHANNELS", "1"))
    input_wav_name: str = os.getenv("INPUT_WAV", "input.wav")

    # Whisper
    whisper_model: str = os.getenv("WHISPER_MODEL", "small")
    whisper_device: str = os.getenv("WHISPER_DEVICE", "cpu")

    # Coqui TTS
    tts_model: str = os.getenv("TTS_MODEL", "tts_models/en/ljspeech/glow-tts")
    tts_use_gpu: bool = _get_bool("TTS_USE_GPU", False)
    tts_sample_rate: int = int(os.getenv("TTS_SAMPLE_RATE", "22050"))

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()

# Ensure directories exist
for _dir in (
    settings.voice_input_dir,
    settings.voice_output_dir,
    settings.transcript_dir,
    settings.recorded_voice_dir,
):
    _dir.mkdir(parents=True, exist_ok=True)



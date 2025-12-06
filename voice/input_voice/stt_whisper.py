from pathlib import Path
from typing import Union

import whisper

from voice.config import settings


AudioPath = Union[str, Path]

print(f"⏳ Loading Whisper model '{settings.whisper_model}' on device '{settings.whisper_device}'...")
model = whisper.load_model(settings.whisper_model, device=settings.whisper_device)
print("✅ Whisper model loaded.")


def speech_to_text(audio_file: AudioPath) -> str:
    """
    Convert speech in an audio file to text using Whisper.
    """
    audio_path = Path(audio_file)
    if not audio_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"🧠 Transcribing {audio_path} ...")
    # Try to be tolerant of short/quiet utterances and force language to English.
    result = model.transcribe(
        str(audio_path),
        language="en",
        no_speech_threshold=0.0,
        condition_on_previous_text=False,
        temperature=0.0,
    )
    text = result.get("text", "").strip()

    if not text:
        print("⚠️ Whisper did not detect any speech in this recording.")
        segments = result.get("segments") or []
        print(f"   segments: {segments}")

    print(f"📝 Recognized Text: {text}")
    return text


if __name__ == "__main__":
    # Example usage (expects a WAV file path)
    default_path = settings.voice_input_dir / settings.input_wav_name
    if default_path.exists():
        speech_to_text(default_path)
    else:
        print(f"⚠️ No default audio file found at {default_path}")



from datetime import datetime
from pathlib import Path
from typing import Optional

import pyttsx3

from voice.config import settings


_engine: Optional[pyttsx3.Engine] = None


def _get_engine() -> pyttsx3.Engine:
    global _engine  # noqa: PLW0603
    if _engine is None:
        print("⏳ Initialising local TTS engine (pyttsx3)...")
        _engine = pyttsx3.init()
        # Optional: adjust speaking rate / volume here if desired
        # _engine.setProperty("rate", 180)
        print("✅ TTS engine initialised.")
    return _engine


def text_to_speech(text: str, save_to_file: bool = True) -> Optional[Path]:
    """
    Convert text to speech using the system TTS engine (pyttsx3),
    play it via speakers, and optionally save to voice/output_voice.

    Returns the Path to the saved audio file if save_to_file is True, else None.
    """
    if not text.strip():
        print("⚠️ Empty text, nothing to speak.")
        return None

    engine = _get_engine()

    output_path: Optional[Path] = None
    if save_to_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Save TTS output into the dedicated recorded_voice directory.
        output_path = settings.recorded_voice_dir / f"tts_{timestamp}.wav"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Queue save-to-file; actual writing happens on runAndWait()
        engine.save_to_file(text, str(output_path))

    # Queue speaking and run
    print("🗣️ Speaking text via system TTS engine...")
    engine.say(text)
    engine.runAndWait()
    print("✅ Finished playback.")

    if save_to_file and output_path is not None:
        print(f"💾 Saved synthesized audio to {output_path}")

    return output_path


if __name__ == "__main__":
    text_to_speech("Hello, this is a test of the local TTS system.")


from datetime import datetime
from pathlib import Path

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

from voice.config import settings


def _resolve_input_path(filename: str | Path | None) -> Path:
    """
    Resolve the recording path into the configured input_voice directory.
    If filename is None, generate a timestamped name.
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"input_{timestamp}.wav"

    path = Path(filename)
    if not path.is_absolute():
        # Keep recordings inside a dedicated subfolder for better organisation.
        recordings_dir = settings.voice_input_dir / "recordings"
        recordings_dir.mkdir(parents=True, exist_ok=True)
        path = recordings_dir / path
    return path


def record_audio(filename: str | Path | None = None, duration: int = 5) -> Path:
    """
    Record audio from the default microphone into voice/input_voice.

    Returns the full Path to the recorded WAV file.
    """
    filepath = _resolve_input_path(filename)
    fs = settings.sample_rate
    channels = settings.channels

    print(f"🎤 Recording for {duration} seconds at {fs} Hz, {channels} channel(s)...")
    print(f"   Target file: {filepath}")

    audio = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()

    # Convert to int16 for WAV storage
    if not np.issubdtype(audio.dtype, np.integer):
        audio = (audio * 32767).astype("int16")

    filepath.parent.mkdir(parents=True, exist_ok=True)
    write(str(filepath), fs, audio)

    print(f"✅ Saved recording as {filepath}")
    return filepath


def check_mic_status(duration: float = 1.0) -> None:
    """
    Simple microphone status check, printed in the terminal.

    - Lists available audio devices and the current default.
    - Records a short test clip (no file saved).
    - Prints whether any signal was detected.
    """
    print("🎧 Audio devices:")
    try:
        devices = sd.query_devices()
        for idx, dev in enumerate(devices):
            print(f"  [{idx}] {dev['name']} (max input channels: {dev['max_input_channels']})")
    except Exception as exc:  # noqa: BLE001
        print(f"❌ Could not query audio devices: {exc}")
        return

    print(f"\nDefault device (input, output): {sd.default.device}")

    fs = settings.sample_rate
    channels = settings.channels
    print(f"\n🎤 Recording a {duration}-second test at {fs} Hz, {channels} channel(s)...")

    audio = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()

    # Compute simple signal metrics
    audio_float = audio.astype("float32") / (32767.0 if np.issubdtype(audio.dtype, np.integer) else 1.0)
    peak = float(np.abs(audio_float).max())
    rms = float(np.sqrt(np.mean(audio_float**2)))

    print(f"📊 Mic test levels -> peak: {peak:.4f}, RMS: {rms:.4f}")

    if peak < 1e-4 and rms < 1e-5:
        print("⚠️ No significant audio detected. Check:")
        print("   - macOS microphone permissions for your terminal")
        print("   - correct input device selection")
        print("   - mic not muted / gain not at zero")
    else:
        print("✅ Audio signal detected from the microphone.")


if __name__ == "__main__":
    # Quick manual test
    check_mic_status(duration=2.0)


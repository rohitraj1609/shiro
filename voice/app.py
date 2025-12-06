from pathlib import Path

from voice.config import settings
from voice.input_voice.audio_io import check_mic_status, record_audio
from voice.input_voice.stt_whisper import speech_to_text
from voice.output_voice.tts_coqui import text_to_speech
from voice.storage import list_transcripts, load_transcript, save_text


def _prompt_int(prompt: str, default: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("❌ Please enter a valid integer.")


def record_and_transcribe() -> None:
    duration = _prompt_int("⏱ How many seconds to record? (e.g., 5): ", default=5)
    audio_path: Path = record_audio(duration=duration)
    text = speech_to_text(audio_path)
    save_text(text, source_audio=audio_path)


def speak_latest_transcript() -> None:
    files = list_transcripts()
    if not files:
        print("❌ No transcripts found.")
        return

    latest = files[-1]
    print(f"📄 Using latest transcript: {latest.name}")
    text = load_transcript(latest)
    print("📝 Text:\n", text)
    text_to_speech(text)


def choose_and_speak_transcript() -> None:
    files = list_transcripts()
    if not files:
        print("❌ No transcripts found.")
        return

    print("📂 Available transcripts:")
    for i, f in enumerate(files, start=1):
        print(f"{i}. {f.name}")

    idx = _prompt_int("Select number: ") - 1
    if idx < 0 or idx >= len(files):
        print("❌ Invalid selection.")
        return

    filename = files[idx]
    text = load_transcript(filename)
    print("📝 Text:\n", text)
    text_to_speech(text)


def main_menu() -> None:
    print(f"=== {settings.app_name} (voice ↔ text, local) ===")
    print(f"Input voice dir      : {settings.voice_input_dir}")
    print(f"Recorded input dir   : {settings.voice_input_dir / 'recordings'}")
    print(f"Recorded voice (TTS) : {settings.recorded_voice_dir}")
    print(f"Transcripts dir      : {settings.transcript_dir}")

    while True:
        print("\n==== Menu ====")
        print("1. Record voice and transcribe")
        print("2. Speak latest transcript")
        print("3. Choose and speak a transcript")
        print("4. Check microphone status")
        print("5. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            record_and_transcribe()
        elif choice == "2":
            speak_latest_transcript()
        elif choice == "3":
            choose_and_speak_transcript()
        elif choice == "4":
            check_mic_status()
        elif choice == "5":
            print("👋 Bye!")
            break
        else:
            print("❌ Invalid choice, try again.")


if __name__ == "__main__":
    main_menu()



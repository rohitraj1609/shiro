## Voice ↔ Text Assistant (Local, Offline)

This project is a small **local voice assistant** written in Python. It lets you:

- **Record** your voice from the microphone
- **Transcribe** speech → text with **Whisper** (local)
- **Save** transcripts to timestamped `.txt` files
- **Speak** text → voice using the system TTS engine (via `pyttsx3`)
- **Check** microphone status and signal levels

Everything runs **offline** on your machine.

---

### 1. Project layout

- `app.py`  
  Root entry point. Starts the CLI menu by calling `voice.app.main_menu()`.

- `voice/`
  - `config.py` – loads settings from `.env` / `dev.yaml` and defines paths
  - `app.py` – main CLI menu and orchestration
  - `storage.py` – save/list/load transcript `.txt` files
  - `input_voice/`
    - `audio_io.py` – microphone recording + mic status check
    - `stt_whisper.py` – speech-to-text using Whisper
  - `output_voice/`
    - `tts_coqui.py` – text-to-speech using the system TTS via `pyttsx3`

- `voice/input_voice/recordings/`  
  All **raw microphone recordings** (`input_YYYYMMDD_HHMMSS.wav`).

- `recorded_voice/`  
  All **generated TTS audio** (`tts_YYYYMMDD_HHMMSS.wav`).

- `transcripts/`  
  Timestamped transcript files (`transcript_YYYYMMDD_HHMMSS.txt`) that contain:

  ```text
  # source_audio: /full/path/to/original_recording.wav

  Recognized text...
  ```

---

### 2. Installation

From the project root:

```bash
pip3 install -r requirements.txt
```

Required Python packages (from `requirements.txt`):

- `openai-whisper` – STT model
- `sounddevice` – microphone input
- `scipy`, `numpy` – audio utilities
- `python-dotenv` – environment config
- `ffmpeg` – Python wrapper; Whisper still uses the system `ffmpeg` binary
- `pyttsx3` – local TTS (uses system voices)

On macOS you also need the **system `ffmpeg`** binary:

```bash
brew install ffmpeg
```

Make sure your terminal / IDE has **microphone permission** in  
System Settings → Privacy & Security → Microphone.

---

### 3. Running the app

From the project root:

```bash
python3 app.py
```

You will see a menu:

```text
1. Record voice and transcribe
2. Speak latest transcript
3. Choose and speak a transcript
4. Check microphone status
5. Exit
```

#### Option 4 – Check microphone status

- Lists all audio devices and shows the **default input/output**.
- Records a 1-second test (not saved).
- Prints the **peak** and **RMS** levels:
  - If very low → no signal (check permissions, device, mute).
  - If non-zero → mic is working.

#### Option 1 – Record voice and transcribe

1. Asks for duration (seconds).
2. Records from the mic → saves to `voice/input_voice/recordings/input_...wav`.
3. Sends the WAV to Whisper → gets text.
4. Saves a transcript to `transcripts/transcript_...txt` with a reference to the source audio.

#### Option 2 – Speak latest transcript

1. Loads the most recent transcript file.
2. Prints the text.
3. Uses `pyttsx3` (system TTS) to:
   - **Speak** the text through your speakers.
   - Save a WAV copy to `recorded_voice/tts_...wav`.

#### Option 3 – Choose and speak a transcript

- Lists all transcripts with numbers.
- Lets you pick one and then performs the same TTS flow as option 2.

---

### 4. Git ignore behavior

The repository includes a `.gitignore` that excludes:

- `recorded_voice/` – generated TTS audio
- `voice/input_voice/recordings/` – raw mic recordings
- `transcripts/` – generated transcript files

This keeps the repo clean and avoids committing large or private audio/text artifacts.



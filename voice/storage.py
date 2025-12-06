from datetime import datetime
from pathlib import Path
from typing import List, Optional

from voice.config import settings


def save_text(text: str, source_audio: Optional[Path] = None) -> Path:
    """
    Save text to a timestamped .txt file in the configured transcripts folder.
    Optionally records the source audio path as a header comment.

    Returns the full Path to the saved file.
    """
    settings.transcript_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = settings.transcript_dir / f"transcript_{timestamp}.txt"

    header_lines = []
    if source_audio is not None:
        header_lines.append(f"# source_audio: {source_audio}")

    with filename.open("w", encoding="utf-8") as f:
        if header_lines:
            f.write("\n".join(header_lines) + "\n\n")
        f.write(text)

    print(f"💾 Saved transcript to {filename}")
    return filename


def list_transcripts() -> List[Path]:
    """
    List transcript files (sorted by name, which includes timestamp).
    """
    settings.transcript_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(settings.transcript_dir.glob("transcript_*.txt"))
    return files


def load_transcript(path_or_name: str | Path) -> str:
    """
    Read text from a transcript file.
    Accepts either a full Path or just a filename.
    """
    path = Path(path_or_name)
    if not path.is_absolute():
        path = settings.transcript_dir / path

    if not path.is_file():
        raise FileNotFoundError(f"Transcript not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    # Quick test
    p = save_text("Hello from test.")
    print(list_transcripts())
    print(load_transcript(p))



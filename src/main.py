from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.transcribe import transcribe_audio, format_text
from src.sheets import sheet_connect, upload_result
from src.text_review import analyze_call

DIR_AUDIO = Path(__file__).parent.parent / "data" / "audio"
DIR_TEXT = Path(__file__).parent.parent / "data" / "text"


def main():
    sheet = sheet_connect()

    for audio in DIR_AUDIO.glob("*"):
        print(audio.name)

        transcribe = transcribe_audio(audio)
        text = format_text(transcribe)

        out_file = DIR_TEXT / f"{audio.stem}.txt"
        out_file.write_text(text, encoding="utf-8")

        analyze = analyze_call(text)

        upload_result(sheet, text, analyze)


if __name__ == "__main__":
    main()
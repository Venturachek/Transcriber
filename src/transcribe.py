from faster_whisper import WhisperModel
from pathlib import Path
import requests
from src.config import settings

model = WhisperModel("medium", device="cpu", compute_type="int8")

def transcribe_audio(audio_path: Path):
    parts, _ = model.transcribe(str(audio_path), language="uk", beam_size=5)
    return " ".join([part.text for part in parts])


def format_text(text: str) -> str:
    prompt = f"""Відформатуй транскрипцію телефонного дзвінка.

ПРАВИЛА:
- Розстав розділові знаки
- Розбий текст на репліки з нового рядка
- Визнач спікера: "Менеджер:" або "Клієнт:"
- Виправ очевидні помилки транскрипції (OCR/ASR помилки, суржик, неправильні слова)
- Якщо слово не існуэ в українській мові, виправ його
- Якщо неможливо зрозуміти слово навіть приблизно — залиш [нерозбірливо], НЕ вигадуй
- Не додавай нові слова, яких не було в оригіналі по змісту
- Не змінюй зміст речень


ВАЖЛИВО:
- Можна виправляти форму слова, але не сенс
- Можна замінювати тільки очевидно зіпсовані слова на найбільш імовірні за контекстом
- Заборонено вигадувати нові факти або нові слова

ТЕКСТ:
{text}

ПОВЕРНИ ТІЛЬКИ ВІДФОРМАТОВАНИЙ ТЕКСТ БЕЗ ПОЯСНЕНЬ."""

    response = requests.post(
        settings.ollama_url,
        json={
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=300
    )

    return response.json()["response"].strip()
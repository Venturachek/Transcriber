# Transcriber

Автоматична транскрибація телефонних дзвінків з оцінкою якості роботи менеджера та вивантаженням результатів у Google Sheets.

## Як це працює

1. Кладеш аудіофайл у папку `data/audio/`
2. **faster-whisper** транскрибує аудіо в текст
3. **Ollama (qwen2.5:14b)** форматує текст і аналізує дзвінок за критеріями
4. Результат записується в Google Sheets з підсвічуванням проблемних дзвінків

## Стек

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — транскрибація аудіо
- [Ollama](https://ollama.com/) — локальна LLM для аналізу тексту
- [gspread](https://github.com/burnash/gspread) — запис у Google Sheets
- Docker + docker-compose

## Структура проєкту

```
Transcriber/
├── src/
│   ├── main.py          # Точка входу
│   ├── config.py        # Налаштування
│   ├── transcribe.py    # Транскрибація та форматування
│   ├── text_review.py   # Аналіз дзвінка через Ollama
│   ├── sheets.py        # Запис у Google Sheets
│   └── services.py      # Список послуг ТОП-100
├── data/
│   ├── audio/           # Вхідні аудіофайли
│   └── text/            # Результати транскрибації
├── credentials.json     # Google Service Account (не комітити!)
├── .env                 # Змінні середовища (не комітити!)
├── .env.example         # Шаблон змінних середовища
├── docker-compose.yml
└── Dockerfile
```

## Запуск

### 1. Клонувати репозиторій

```bash
git clone https://github.com/Venturachek/Transcriber.git
cd Transcriber
```

### 2. Створити папки

```bash
mkdir -p data/audio data/text
```

### 3. Створити файл .env

Створи файл `.env` у корені проєкту та додай наступні дані:

```env
OLLAMA_HOST=ollama_reviewer
OLLAMA_PORT=11434
SPREADSHEET_ID=your_spreadsheet_id_here
```

### 4. Додати Google credentials

Поклади файл `credentials.json` (Google Service Account) у корінь проєкту.

Як отримати:
1. [Google Cloud Console](https://console.cloud.google.com/) → IAM → Service Accounts
2. Створи сервісний акаунт → додай роль Editor
3. Створи ключ у форматі JSON
4. Відкрий доступ до таблиці для email сервісного акаунта

### 5. Створити Docker мережу

```bash
docker network create newNetwork
```

### 6. Запустити

```bash
docker compose up --build -d
```

### 7. Завантажити модель Ollama (перший раз)

```bash
docker exec -it ollama_reviewer ollama pull qwen2.5:14b
```

### 8. Додати аудіофайли та запустити обробку

Скопіюй `.mp3` або `.wav` файли в папку `data/audio/` та запусти вручну:

```bash
docker exec -it audio_transcriber python src/main.py
```

## Моніторинг

```bash
# Логи в реальному часі
docker compose logs -f transcriber

# Статус контейнерів
docker compose ps
```

## Критерії оцінки дзвінка

| Критерій | Опис |
|---|---|
| Початок розмови | Менеджер привітався та назвав себе або сервіс |
| Модель авто | Модель авто була названа |
| Рік авто | Рік авто був названий |
| Пробіг | Пробіг був названий |
| Комплексна діагностика | Менеджер запропонував діагностику |
| Раніше виконані роботи | Попередні ремонти були згадані |
| Запис на сервіс | Клієнт записався |
| Завершення розмови | Менеджер попрощався |

Оцінка менеджера від 0 до 10. Рядки з оцінкою нижче 5 підсвічуються червоним у таблиці.

## Примітки

- Перший запуск довший — faster-whisper завантажує модель `large-v3` (~3GB)
- Модель кешується у Docker volume `whisper_cache` — наступні запуски швидші
- Ollama з моделлю `qwen2.5:14b` потребує ~10GB RAM
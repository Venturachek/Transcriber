FROM python:3.11.9

# ffmpeg нужен для faster-whisper
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


RUN mkdir -p /app/data/audio /app/data/text

CMD ["python", "src/main.py"]
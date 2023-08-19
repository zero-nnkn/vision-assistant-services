# Text-to-speech Service

## Install with Docker
Create `.env` file. You can change model config here
```bash
$ cp .env.example .env
```
Build Docker image:
```bash
$ docker build -t text_to_speech_api .
```

## Run container with GPU access
```bash
$ docker run -it --gpus all -p 8001:8001 text_to_speech_api
```
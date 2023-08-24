# Text-to-Speech Service

## Install with Docker
Create `.env` file. You can change model config here
```bash
cp .env.example .env
```
Build Docker image:
```bash
docker build -t text_to_speech_api .
```

Note: If you want to run tests, uncomment libs for testing in `requirements.txt` before building and run `pytest` inside the running container.

## Run container with GPU access
```bash
docker run -it --gpus all -p 8001:8001 text_to_speech_api
```
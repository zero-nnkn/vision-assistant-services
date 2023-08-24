# Speech-to-Text API

## Install with Docker
Create `.env` file. You can change model config here.
```bash
cp .env.example .env
```

Build Docker image:
```bash
docker build -f Dockerfile.prod -t speech-to-text .
```

Note: If you want to run tests, use the `Dockerfile` and run `pytest` inside the running container.

## Run the API
```bash
docker run -it --gpus all -p 8000:8000 speech-to-text
```
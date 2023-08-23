# Aggregator API
This service pushes the image to S3 bucket, and concurrently invoke other three services to process the image
## Install with Docker
Create an `.env` file, remember to fill in the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables
```bash
$ cp .env.example .env
```
Build Docker image:
```bash
$ docker build -t aggregator_service .
```

## Run the API
```bash
$ docker run -it -p 8000:8000 aggregator_service:latest
```


# Feedback API with AWS Lambda
This folder contains code needed to create a serverless API that receives and stores user's feedback. The structure of the folder is as follow:
- `main.py` - Main code for the Lambda function
- `Dockerfile` - The Dockerfile that uses base Lambda base image from AWS to create an image for local testing
- `requirements.txt` - Pip requirements

## Build and run Docker image for local testing
Prerequisite:
- Docker is installed

Build Docker image. Remember to replace `AWS_REGION` and `TABLE_NAME` according to your setup
```bash
$ docker build -t feedback_service --build-arg AWS_REGION=<your_lambda_region> TABLE_NAME=<your_table_name>
```

Start a container by Docker run:
```bash
$ docker run -p 8080:8080 feedback_service:latest
```
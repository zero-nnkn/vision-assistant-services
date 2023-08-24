# Aggregator API
This service is an entrypoint for our system following the `Aggregator` design pattern. It receives clients' requests, invokes other microservices, aggregates their outputs, and responds to clients.
## Install with Docker
Create a `.env` file, remember to fill in the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables
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


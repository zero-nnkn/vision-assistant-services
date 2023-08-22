# Speech-to-Text API
## Local Development
### Install
Create `.env` file. You can change model config here.
```
cp .env.example .env
```

Run with Docker: Use `Dockerfile`
```
docker-compose up -d --build
```

### Test
```
docker compose exec speech-to-text pytest
```

## Production
Use `Dockerfile.prod` instead of `Dockerfile` (change `docker-compose.yml` if you want run with Docker Compose).
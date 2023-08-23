from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from src.config import settings
from src.tts.router import init_transcripber
from src.tts.router import router as tts_router

app = FastAPI(title="Text-to-speech API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_headers=settings.CORS_HEADERS,
    allow_credentials=True,
    allow_methods=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Get the original 'detail' list of errors
    details = exc.errors()
    error_details = []

    for error in details:
        error_details.append({"error": error["msg"] + " " + str(error["loc"])})
    return JSONResponse(content={"message": error_details})


@app.on_event("startup")
async def startup_event():
    init_transcripber(
        model_path=settings.MODEL_PATH,
        config_path=settings.CONFIG_PATH,
        vocoder_path=settings.VOCODER_PATH if settings.VOCODER_PATH != "" else None,
        vocoder_config=settings.VOCODER_CONFIG_PATH if settings.VOCODER_CONFIG_PATH != "" else None,
        device=settings.MODEL_DEVICE,
    )


@app.get("/", include_in_schema=False)
async def root() -> None:
    return RedirectResponse("/docs")


@app.get("/health", status_code=status.HTTP_200_OK, tags=["health"])
async def perform_healthcheck() -> None:
    return JSONResponse(content={"message": "success"})


app.include_router(tts_router, prefix="/tts")

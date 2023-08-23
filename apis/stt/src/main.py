from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from src.config import settings
from src.stt.router import init_transcripber
from src.stt.router import router as stt_router

app = FastAPI(title="Speech-to-Text API")


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
        error_details.append({"error": f"{error['msg']} {str(error['loc'])}"})
    return JSONResponse(content={"message": error_details})


@app.on_event("startup")
async def startup_event():
    init_transcripber(
        model_path=settings.FASTER_WHISPER_MODEL,
        device=settings.FASTER_WHISPER_MODEL_DEVICE,
        compute_type=settings.FASTER_WHISPER_MODEL_COMPUTE_TYPE,
    )


@app.get("/", include_in_schema=False)
async def root() -> None:
    return RedirectResponse("/docs")


@app.get("/health", status_code=status.HTTP_200_OK, tags=["health"])
async def perform_healthcheck() -> None:
    return JSONResponse(content={"message": "success"})


app.include_router(stt_router, prefix="/stt")


# Run API
# if __name__ == '__main__':
#     import uvicorn

#     uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, reload=True)

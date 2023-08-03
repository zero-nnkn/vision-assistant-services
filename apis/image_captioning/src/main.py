import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from config import settings
from image_captioning.router import router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_headers=settings.CORS_HEADERS,
    allow_credentials=True,
    allow_methods=["*"],
)


@app.get("/")
async def docs_redirect():
    return RedirectResponse("/docs")


@app.get("/health")
async def perform_healthcheck():
    """[FastAPI endpoint]
    To ensure the API is working.
    """
    return {"message": "success"}


app.include_router(router, tags=["Image Captioning"], prefix="/captioning")


def main():
    # run server with uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,  # Uncomment this for debugging
    )


if __name__ == "__main__":
    main()

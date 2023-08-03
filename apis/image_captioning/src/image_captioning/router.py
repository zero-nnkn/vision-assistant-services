import torch
from config import settings
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

from .predictor import ImageCaptioner

router = APIRouter()

captioner = ImageCaptioner(
    model_path=settings.MODEL_PATH,
    processor_path=settings.MODEL_PATH,
    tokenizer_path=settings.MODEL_PATH,
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
)


@router.post("/predict/")
async def generate_caption(image_file: UploadFile) -> JSONResponse:
    """[FastAPI endpoint]
    Generate a caption for an uploaded image.

    Args:
        image_file (File): Uploaded Image file

    Returns:
        Response (JSONResponse): message and caption of the image (if there is no exception)

    """
    try:
        image = Image.open(image_file.file)
        caption = captioner.predict(image)
    except Exception:
        raise HTTPException(status_code=422, detail="Cannot process entity")

    return JSONResponse(content={"message": "success", "caption": caption})

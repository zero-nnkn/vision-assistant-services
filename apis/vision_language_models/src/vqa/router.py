import sys
from io import BytesIO

from fastapi import APIRouter, File
from fastapi.responses import JSONResponse
from PIL import Image

from .predictors import *

router = APIRouter()
predictor = None


def init(settings):
    global predictor
    cls = getattr(sys.modules[__name__], settings.PREDICTOR_NAME)
    predictor = cls()


@router.post('/answer')
def answer(image_file: bytes = File(), prompt: str = "") -> JSONResponse:
    image = Image.open(BytesIO(image_file)).convert("RGB")
    try:
        output = predictor.answer(image, prompt)
    except Exception:
        import traceback

        traceback.print_exc()
        return JSONResponse(content={"message": "VQA error"})

    return JSONResponse(content={"message": "success", "answer": output})

import sys
from io import BytesIO

from fastapi import APIRouter, File
from fastapi.responses import JSONResponse
from PIL import Image

from .predictors import *
from .utils import S3ObjectQuery

router = APIRouter()
predictor = None
s3_object_query = None


def init(settings):
    """
    Initialize the VQA model and S3 service
    """
    global predictor, s3_object_query
    cls = getattr(sys.modules[__name__], settings.PREDICTOR_NAME)
    args = eval(settings.PREDICTOR_ARGS)
    predictor = cls(device=settings.DEVICE, **args)

    s3_object_query = S3ObjectQuery(
        settings.S3_BUCKET_NAME,
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
    )


@router.post('/answer')
def answer(
    image_file: bytes = File(default=None),
    image_filename: str = "",
    prompt: str = "Describe this picture",
) -> JSONResponse:
    """
    Answer the prompt based on the image's content
    Args:
        image_file: image file in bytes
        image_filename: filename of the image stored on S3, to be used if the image_file is not specified
        prompt: Text prompt to retrieve information from the image
    Return:
        A response in json format.
            + If successfully: {"message": "success", "answer": output}
            + else if an error occurs: {"message": "VQA error"}
    """
    try:
        # Request file from S3 if image_file is not specified
        if image_file is None:
            image_file = s3_object_query.query(image_filename)

        image = Image.open(BytesIO(image_file)).convert("RGB")
        output = predictor.answer(image, prompt)
    except Exception:
        import traceback

        traceback.print_exc()
        return JSONResponse(content={"message": "VQA error"})

    return JSONResponse(content={"message": "success", "answer": output})

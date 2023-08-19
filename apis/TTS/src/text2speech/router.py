from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from .service import Transcriber


class Item(BaseModel):
    text: str


router = APIRouter()

transcripber = None


def init_transcripber(**kargs):
    """
    Initialize the transcriber as a singleton object.
    Use at API startup.
    """
    global transcripber
    if transcripber is None:
        transcripber = Transcriber(**kargs)


@router.post("/transcription/text")
def transcribe(item: Item):
    """
    The function transcribes a text and returns a audio in a File response.
    """
    try:
        transcripber.transcribe(item.text)
    except Exception:
        return JSONResponse(status_code=500, content={"message": "Transcribe error"})
    else:
        return FileResponse("/tmp/output.wav", media_type="audio/mpeg", status_code=200)

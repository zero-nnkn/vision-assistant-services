from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from src.tts.service import Transcriber


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

    Args:
      item (Item): An object contains information about the text that needs to be transcribed.

    Returns:
      A File response contains the audio file
      or a JSON response if there is an error.
    """
    try:
        transcripber.transcribe(item.text)
    except ValueError:
        return JSONResponse(
            status_code=422, content={"message": "Invalid input text (e.g. empty text etc.)"}
        )
    except Exception:
        return JSONResponse(status_code=500, content={"message": "Transcribe error"})
    else:
        return FileResponse("/tmp/output.wav", media_type="audio/mpeg", status_code=200)

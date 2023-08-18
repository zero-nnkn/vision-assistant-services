import datetime
import os

from fastapi import APIRouter, File
from fastapi.responses import JSONResponse, StreamingResponse

from .service import Transcriber

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


@router.post('/transcription/text')
def transcribe(text: str = ""):
    """
    The function transcribes a text and returns a audio in a Streaming response.
    """
    try:
        transcripts = transcripber.transcribe(text)
    except Exception:
        return JSONResponse(content={'message': 'transcribe error'})

    return StreamingResponse(transcripts, media_type='video/mp4')

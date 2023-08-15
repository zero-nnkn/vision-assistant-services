import io

from fastapi import APIRouter, File
from fastapi.responses import JSONResponse

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


@router.post('/transcription/audio')
async def transcribe(audio_file: bytes = File()) -> JSONResponse:
    audio_file = io.BytesIO(audio_file)

    try:
        transcripts = transcripber.transcribe(audio_file, beam_size=5)
    except Exception:
        return JSONResponse(content={'message': 'transcribe error'})

    return JSONResponse(
        content={
            'message': 'success',
            'transcripts': transcripts,
        }
    )

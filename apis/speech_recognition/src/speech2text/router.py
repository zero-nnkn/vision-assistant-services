import datetime
import os

from fastapi import APIRouter, File
from fastapi.responses import JSONResponse

from .service import Transcriber

router = APIRouter()


transcripber = Transcriber(
    model_size='small',
    device='cpu',
    compute_type='float32',
)


@router.post('/transcription/audio')
def transcribe(audio_file: bytes = File()) -> JSONResponse:
    """
    The function transcribes an audio file and returns the transcripts in a JSON response.
    """
    audio_path = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H%M-%S")}.mp3'
    with open(audio_path, 'wb') as f:
        f.write(audio_file)

    try:
        transcripts = transcripber.transcribe(audio_path, beam_size=5)
    except Exception:
        return JSONResponse(content={'message': 'transcribe error'})

    os.remove(audio_path)

    return JSONResponse(
        content={
            'message': 'success',
            'transcripts': transcripts,
        }
    )

import io

from fastapi import APIRouter, File, status
from fastapi.responses import JSONResponse
from src.speech2text.service import Transcriber

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
    """
    The function transcribes an audio file and returns the transcripts as a JSON response.

    Args:
      audio_file (bytes): The `audio_file` parameter is of type `bytes` and represents the audio file
    that needs to be transcribed. It is expected to be passed as a file in the request body.

    Returns:
      A JSON response has the following structure:
      {
          'info': {
              'language': 'en',
              'language_probability': 0.99,
          },
          'segments': [
              {'start': 0.0, 'end': 0.5, 'text': 'Hello world.'},
              {'start': 0.5, 'end': 1.0, 'text': 'How are you?'},
          ],
      }
    """
    audio_file = io.BytesIO(audio_file)

    try:
        transcripts = transcripber.transcribe(audio_file, beam_size=5)
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'message': 'transcribe error'},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'message': 'success',
            'info': transcripts['info'],
            'segments': transcripts['segments'],
        },
    )

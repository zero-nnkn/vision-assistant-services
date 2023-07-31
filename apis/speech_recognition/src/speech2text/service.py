from functools import lru_cache

from faster_whisper import WhisperModel


class Transcriber:
    """
    Transcriber class to transcribe audio file to text using pretrained Faster Whisper.
    """

    def __init__(
        self, model_size: str = 'base', device: str = 'cpu', compute_type: str = 'float32'
    ):
        self.load_model(model_size=model_size, device=device, compute_type=compute_type)

    @lru_cache(maxsize=1)
    def load_model(
        self, model_size: str = 'base', device: str = 'cpu', compute_type: str = 'float32'
    ):
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(
        self,
        audio_path: str,
        beam_size: int = 5,
    ):
        segments, info = self.model.transcribe(audio_path, beam_size=beam_size)
        result = {
            'info': {
                'language': info.language,
                'language_probability': info.language_probability,
            },
            'segments': [
                {'start': segment.start, 'end': segment.end, 'text': segment.text}
                for segment in segments
            ],
        }
        return result

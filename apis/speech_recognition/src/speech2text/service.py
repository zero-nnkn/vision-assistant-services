from functools import lru_cache
from typing import BinaryIO, Union

import numpy as np
from faster_whisper import WhisperModel


class Transcriber:
    """
    Transcriber class to transcribe audio file to text using pretrained Faster Whisper.
    """

    def __init__(
        self, model_size: str = 'base', device: str = 'cpu', compute_type: str = 'float32'
    ):
        """
        Initialize the Whisper model.
        """
        self._load_model(model_size=model_size, device=device, compute_type=compute_type)

    @lru_cache(maxsize=1)
    def _load_model(
        self, model_size: str = 'base', device: str = 'cpu', compute_type: str = 'float32'
    ):
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(
        self,
        audio: Union[str, BinaryIO, np.ndarray],
        beam_size: int = 5,
    ):
        """
        Transcribes an input file.

        Args:
          audio: Path to the input file (or a file-like object), or the audio waveform.
          beam_size: Beam size to use for decoding.

        Returns:
          A dictionary with the following structure:
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
        segments, info = self.model.transcribe(audio, beam_size=beam_size)
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

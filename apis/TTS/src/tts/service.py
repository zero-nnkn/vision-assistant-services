from functools import lru_cache

import torch
from TTS.api import TTS


class Transcriber:
    """
    Transcriber class to transcribe text to audio file
    """

    def __init__(
        self,
        model_name: str = None,
        model_path: str = None,
        config_path: str = None,
        vocoder_path: str = None,
        vocoder_config: str = None,
        device: str = "cpu",
    ):
        if model_name is not None:
            self.load_model_by_name(model_name=model_name, device=device)
        elif model_path is not None:
            self.load_model_by_path(
                model_path, config_path, vocoder_path, vocoder_config, device=device
            )

    @lru_cache(maxsize=1)
    def load_model_by_name(
        self, model_path: str = "tts_models/en/ljspeech/vits", device: str = "cpu"
    ):
        if device == "gpu" and not torch.cuda.is_available():
            print("No CUDA device is available")
            device = "cpu"
        self.model = TTS(model_path=model_path, gpu=True if device == "gpu" else False)

    @lru_cache(maxsize=1)
    def load_model_by_path(
        self,
        model_path: str,
        config_path: str,
        vocoder_path: str,
        vocoder_config: str,
        device: str = "cpu",
    ):
        if device == "gpu" and not torch.cuda.is_available():
            print("No CUDA device is available")
            device = "cpu"
        self.model = TTS(
            model_path=model_path,
            config_path=config_path,
            vocoder_path=vocoder_path,
            vocoder_config_path=vocoder_config,
            gpu=True if device == "gpu" else False,
        )

    def transcribe(
        self,
        text: str,
    ):
        """
        Convert the text to speech and save it as a WAV file.

        Args:
          text (str): string that represents the text that needs to be transcribed.
        """

        def __preprocess_input(s: str):
            return s.strip()

        text = __preprocess_input(text)
        if not text:  # empty
            raise ValueError("Empty text")

        self.model.tts_to_file(text=text, file_path="/tmp/output.wav")

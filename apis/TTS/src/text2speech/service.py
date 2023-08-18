from functools import lru_cache

import torch
from TTS.api import TTS


class Transcriber:
    """
    Transcriber class to transcribe audio file to text using pretrained Faster Whisper.
    """

    def __init__(self, model_name: str = 'tts_models/en/ljspeech/vits', device: str = 'cpu'):
        self.load_model(model_name=model_name, device=device)

    @lru_cache(maxsize=1)
    def load_model(self, model_name: str = 'tts_models/en/ljspeech/vits', device: str = 'cpu'):
        if device == 'gpu' and not torch.cuda.is_available():
            print("No CUDA device is available")
            device = 'cpu'
        self.model = TTS(model_name, gpu=True if device == 'gpu' else False)

    def transcribe(
        self,
        text: str,
    ):
        self.model.tts_to_file(text=text, file_path="./output.mp4")
        res_data = open('./output.mp4', 'rb')
        # result = {
        #     'speech': res_data
        # }
        return res_data

import torch

from PIL import Image
from functools import lru_cache
from transformers import ViTImageProcessor, VisionEncoderDecoderModel, AutoTokenizer


class ImageCaptioner:
    """Image Captioning predictor"""

    def __init__(
        self,
        model_path: str,
        processor_path: str,
        tokenizer_path: str,
        device=torch.device("cpu"),
    ):
        self.device = device
        self.load_models(
            model_path=model_path,
            processor_path=processor_path,
            tokenizer_path=tokenizer_path,
        )

    @lru_cache
    def load_models(
        self, model_path: str, processor_path: str, tokenizer_path: str
    ) -> None:
        """
        Load HuggingFace model, processor, and tokenizer from Model Hub or local.
        If the local path does not exist, it will search on the HuggingFace Hub
        """

        try:
            self.model = VisionEncoderDecoderModel.from_pretrained(model_path)
            self.processor = ViTImageProcessor.from_pretrained(processor_path)
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
            self.model.to(self.device)
        except Exception:
            raise Exception("Model loading error")

    def predict(
        self, image: Image.Image, gen_kwargs: dict = {"max_length": 16, "num_beams": 4}
    ) -> str:
        """
        Receive an image and generate a caption

        Args:
            image (PIL.Image.Image): Image to predict
            gen_kwargs (dict): configurations for inference

        Return:
            str: a caption for the input image
        """
        pixel_values = self.processor(images=[image], return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)

        output_ids = self.model.generate(pixel_values, **gen_kwargs)
        preds = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]

        return preds.strip()

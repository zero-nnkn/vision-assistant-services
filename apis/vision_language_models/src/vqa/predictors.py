from typing import List
from PIL import Image
from lavis.models import load_model_and_preprocess


class BasePredictor:
    def __init__(self, device: str) -> None:
        self.device = device
    
    def answer(self, image, prompt):
        raise NotImplementedError("The predictor must implement 'answer()' method")
    
    
class BasicVQA(BasePredictor):
    def __init__(self, device="cuda", name="blip_vqa", model_type="vqav2"):
        super().__init__(device)
        self.model, self.vis_processors, self.txt_processors = load_model_and_preprocess(
            name=name,
            model_type=model_type,
            is_eval=True,
            device=self.device
        )
        
    def answer(self, image: Image.Image, prompt: str) -> str:
        image = self.vis_processors["eval"](image).unsqueeze(0).to(self.device)
        prompt = self.txt_processors["eval"](prompt)
        output = self.model.predict_answers(
            samples={"image": image, "text_input": prompt},
            inference_method="generate"
        )
        return output[0]
        
    
    
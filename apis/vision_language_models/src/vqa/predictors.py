import os
from argparse import Namespace
from pathlib import Path

import imagehash
from minigpt4.common.config import Config
from minigpt4.common.registry import registry
from minigpt4.conversation.conversation import CONV_VISION, Chat
from PIL import Image

ROOT = Path(__file__).parent


def hash_image(image):
    """
    Compute hash value of image based on size and pixels
    Args:
        image: a PIL.Image.Image object to be hashed
    Return:
        A string which is the hash value of the image
    """
    value = str(image.size)
    for method_name in ("average_hash", "phash", "dhash", "whash"):
        method = getattr(imagehash, method_name)
        value += str(method(image))
    return value


class BasePredictor:
    """
    Base class to implement Visual Question Answering predictors
    """

    def __init__(self, device: str) -> None:
        self.device = device

    def answer(self, image: Image.Image, prompt: str) -> str:
        raise NotImplementedError("The predictor must implement 'answer()' method")


class MiniGPT4(BasePredictor):
    def __init__(
        self,
        device: str,
        cfg_path: str = os.path.join(ROOT, "minigpt4_configs/minigpt4_eval.yaml"),
        max_new_tokens: int = 30,
        cache_size: int = 100,
        save_mem_mode=True,
    ):
        """
        Initialize the MiniGPT-4 model
        Args:
            device: Device to store the model, can be "cpu", "cuda"
            cfg_path: Path to the model configuration file
                default: minigpt4_configs/minigpt4_eval.yaml
            max_new_tokens: The maximum tokens to generate answer
                default: 30
            cache_size: Number of embedding tensors to be cached in runtime
            save_mem_mode: Whether to use 8-bit mode to save GPU memory.
                The inference time is also decelerated
        """
        super().__init__(device)
        self.max_new_tokens = max_new_tokens
        self.cache = {}
        self.cached_keys = []
        self.cache_size = cache_size

        args = Namespace(cfg_path=cfg_path, options=None, gpu_id=0)
        cfg = Config(args)
        cfg.model_cfg.low_resource = save_mem_mode

        model_config = cfg.model_cfg
        model_config.device_8bit = args.gpu_id
        model_cls = registry.get_model_class(model_config.arch)
        model = model_cls.from_config(model_config).to(self.device)

        vis_processor_cfg = cfg.datasets_cfg.cc_sbu_align.vis_processor.train
        vis_processor = registry.get_processor_class(vis_processor_cfg.name).from_config(
            vis_processor_cfg
        )
        self.chat = Chat(model, vis_processor, device=self.device)

    def process_image(self, image: Image.Image):
        """
        Compute image's embedding which is fed to the LLM.
        Args:
            image: a PIL.Image.Image object
        Return:
            A tuple of:
                + embedding tensor (torch.Tensor)
                + chat state: State of the conversation understood by the LLM
        """
        # Compute hash value of the image
        # If the image information is cached before, there's no need to process it again
        key = hash_image(image)

        if key not in self.cache:
            embeds = []
            chat_state = CONV_VISION.copy()
            self.chat.upload_img(image, chat_state, embeds)

            self.cache[key] = embeds, chat_state
            self.cached_keys.append(key)
            if len(self.cache) > self.cache_size:
                removed_key = self.cached_keys.pop(0)
                del self.cache[removed_key]
        else:
            embeds, chat_state = self.cache[key]
        return embeds[0], chat_state.copy()

    def answer(self, image: Image.Image, prompt: str) -> str:
        """
        Answer the prompt based on image content
        Args:
            + image: a PIL.Image.Image object
            + prompt: Prompt to retrieve information from the image
        Return:
            A string which is the answer
        """
        embed, chat_state = self.process_image(image)

        self.chat.ask(prompt, chat_state)
        answer = self.chat.answer(
            conv=chat_state,
            img_list=[embed],
            max_new_tokens=self.max_new_tokens,
        )[0]

        # Take the first sentence
        stop_pos = answer.find(".")
        if stop_pos == -1:
            stop_pos = 0
        return answer[:stop_pos].replace("<Img>", "")

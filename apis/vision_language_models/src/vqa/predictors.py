from argparse import Namespace

import imagehash
from minigpt4.common.config import Config
from minigpt4.common.registry import registry
from minigpt4.conversation.conversation import CONV_VISION, Chat
from PIL import Image


def hash_image(image):
    value = str(image.size)
    for method_name in ("average_hash", "phash", "dhash", "whash"):
        method = getattr(imagehash, method_name)
        value += str(method(image))
    return value


class BasePredictor:
    def __init__(self, device: str) -> None:
        self.device = device

    def answer(self, image: Image.Image, prompt: str) -> str:
        raise NotImplementedError("The predictor must implement 'answer()' method")


class MiniGPT4(BasePredictor):
    def __init__(self, device: str, cfg_path: str, max_new_tokens: int = 30, cache_size: int = 100):
        super().__init__(device)
        self.max_new_tokens = max_new_tokens
        self.cache = {}
        self.cached_keys = []
        self.cache_size = cache_size

        args = Namespace(cfg_path=cfg_path, options=None, gpu_id=0)
        cfg = Config(args)

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
        return embeds[0], chat_state

    def answer(self, image: Image.Image, prompt: str) -> str:
        embed, chat_state = self.process_image(image)

        self.chat.ask(prompt, chat_state)
        answer = self.chat.answer(
            conv=chat_state,
            img_list=[embed],
            max_new_tokens=self.max_new_tokens,
        )[0]

        stop_pos = answer.find(".")
        return answer[:stop_pos]

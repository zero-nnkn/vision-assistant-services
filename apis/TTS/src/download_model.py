import os
from pathlib import Path

from dotenv import load_dotenv, set_key
from TTS.utils.manage import ModelManager


def get_model_dir():
    """Get model saved dir"""
    return Path(__file__).parent.parent / "model/"


def get_models_file_path():
    """Get path to the file containing list of models information"""
    return os.path.join(get_model_dir(), ".model.json")


def download_model_by_name(model_name: str = "tts_models/en/ljspeech/vits"):
    """Download and save model to local"""

    model_path, config_path, model_item = manager.download_model(model_name)
    if "fairseq" in model_name or (
        model_item is not None and isinstance(model_item.get("model_url"), list)
    ):
        # return model directory if there are multiple files
        # we assume that the model knows how to load itself
        return None, None, None, None, model_path
    if model_item.get("default_vocoder") is None:
        return model_path, config_path, None, None, None
    vocoder_path, vocoder_config_path, _ = manager.download_model(model_item["default_vocoder"])
    return model_path, config_path, vocoder_path, vocoder_config_path, None


if __name__ == "__main__":
    env_file_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_file_path)

    global manager
    manager = ModelManager(
        models_file=get_models_file_path(),
        output_prefix=get_model_dir(),
        progress_bar=True,
        verbose=False,
    )

    model_name = os.getenv("MODEL_NAME")
    (
        model_path,
        config_path,
        vocoder_path,
        vocoder_config_path,
        model_dir,
    ) = download_model_by_name(model_name)

    # Save variables to .env for later uses
    set_key(dotenv_path=env_file_path, key_to_set="MODEL_PATH", value_to_set=model_path)
    set_key(dotenv_path=env_file_path, key_to_set="CONFIG_PATH", value_to_set=config_path)
    if vocoder_path:
        set_key(
            dotenv_path=env_file_path,
            key_to_set="VOCODER_PATH",
            value_to_set=vocoder_path,
        )
    if vocoder_config_path:
        set_key(
            dotenv_path=env_file_path,
            key_to_set="VOCODER_CONFIG_PATH",
            value_to_set=vocoder_config_path,
        )

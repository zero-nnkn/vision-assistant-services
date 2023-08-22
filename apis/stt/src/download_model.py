from faster_whisper.utils import download_model

if __name__ == "__main__":
    model_path = download_model(
        size_or_id="small",
        output_dir="model/faster-whisper-small",
        local_files_only=False,
    )
    print(model_path)

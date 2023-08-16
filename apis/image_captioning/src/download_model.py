import argparse
import os
from pathlib import Path

import boto3
from dotenv import load_dotenv
from transformers import AutoTokenizer, VisionEncoderDecoderModel, ViTImageProcessor

load_dotenv()


def init_arguments():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--bucket_name", type=str, help="S3 bucket name")
    parser.add_argument("--filename", type=str, help="S3 filename")
    parser.add_argument("--destination", type=str, help="Model save path")
    return parser.parse_args()


def download_model_from_huggingface(source: str, destination: Path):
    """Load model from Hugging Face Model Hub"""
    processor = ViTImageProcessor.from_pretrained(source)
    processor.save_pretrained(destination)
    model = VisionEncoderDecoderModel.from_pretrained(source)
    model.save_pretrained(destination)
    tokenizer = AutoTokenizer.from_pretrained(source)
    tokenizer.save_pretrained(destination)


def download_model_from_S3(bucket_name: str, s3_filename: str, destination: Path) -> None:
    """Load model from S3 bucket"""
    s3 = boto3.client(
        "s3",
        os.getenv("AWS_REGION", "us-west-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        s3.download_file(bucket_name, s3_filename, str(destination))
    except Exception:
        raise Exception(f"Cannot download file {s3_filename} from S3")


def main():
    args = init_arguments()
    download_model_from_S3(args.bucket_name, args.filename, args.destination)

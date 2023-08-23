import io
import json
import uuid

import boto3
import requests
from botocore.exceptions import ClientError
from config import settings

s3 = boto3.resource("s3")


def upload_image_to_S3(s3, image_file_content: bytes, bucket_name: str) -> str:
    """
    The function to upload image to S3 bucket

    Args:
        s3: boto3 resource that is mapped to the AWS S3
        image_file_content (bytes): content of the image file represented in bytes type
        bucket_name (str): name of the S3 bucket

    Return:
        filename: a unique filename to identify the image in S3
    """
    id = uuid.uuid4()
    filename = str(id) + ".jpg"

    try:
        obj = s3.Object(bucket_name, filename)
        obj.put(Body=image_file_content)
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        return filename


def vqa_pipeline(speech: bytes, image: bytes | str):
    """
    Handler method processes client's speech and image.
    It is going to invoke the three microservices sequentially: speech-recognition,
    vision-language model, and text-to-speech.

    Args:
        speech (bytes): audio file content that represents client speech
        image (bytes | str): the image that client wants to ask about
            If the image is bytes type, it will be stored to S3 and processed for the first time.
            If the image is str, assume it is the index,
            the system will query image content from the database
            and process it.
    Return:
        answer_text: answer in text form
        answer_speech: answer in audio form
    """

    # Get the text from the STT service
    stt_endpoint = settings.STT_ENDPOINT
    response = requests.post(stt_endpoint, files={"audio_file": speech})
    if response.status_code != 200:
        raise Exception(f"Speech-to-text failed: {response.text}")

    # Since service responses a list of segments, each segment contains a text,
    # we need to combine them to a single text
    segments = response.json().get("segments")
    text = " ".join([segment.get("text") for segment in segments])

    # Request to the Vision-language service
    vlm_endpoint = settings.VLM_ENDPOINT
    if isinstance(image, str):
        params = {"image_filename": image, "prompt": text}
        response = requests.post(vlm_endpoint, params=params)
    elif isinstance(image, io.BufferedReader) or isinstance(image, bytes):
        params = {"prompt": text}
        response = requests.post(vlm_endpoint, params=params, files={"image_file": image})
    else:
        raise Exception("Invalid input type")
    if response.status_code != 200:
        raise Exception(f"VLM Service failed!: {response.text}")
    answer = response.json()["answer"]

    # Request to the Text-to-speech service
    tts_endpoint = settings.TTS_ENDPOINT
    data = {"text": answer}
    response = requests.post(tts_endpoint, data=json.dumps(data))
    answer_speech = response.content

    # Convert to base64 type since base64 is more efficient for audio to transfer than bytes type
    return {"answer_text": answer, "answer_speech": answer_speech}

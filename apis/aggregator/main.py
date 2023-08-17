import json
import os
import uuid
from concurrent.futures import ThreadPoolExecutor

import boto3
import requests
from botocore.exceptions import ClientError
from dotenv import load_dotenv


def upload_image_to_S3(image_file_content: bytes, bucket_name: str):
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    id = uuid.uuid4()
    filename = str(id) + ".jpg"

    try:
        obj = s3.Object(bucket_name, filename)
        obj.put(image_file_content)
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        return filename


def vqa_handler(speech: bytes, image: bytes | str):
    # Get the text from the STT service
    stt_endpoint = os.environ.get("STT_ENDPOINT")
    response = requests.post(stt_endpoint, files={"audio_file": speech})
    if response.status_code != 200:
        raise Exception(f"Speech-to-text failed: {response.text}")

    text = response.json()["transcripts"]

    # VQA
    vqa_endpoint = os.environ.get("VQA_ENDPOINT")
    if isinstance(image, str):
        data = {"image_file": image, "prompt": text}
        response = requests.post(vqa_endpoint, data=json.dumps(data))
    elif isinstance(image, bytes):
        response = requests.post(
            vqa_endpoint, data=json.dumps({"prompt": text}), files={"image_file": image}
        )
    else:
        raise Exception("Invalid image type")
    if response.status_code != 200:
        raise Exception(f"VQA Service failed!: {response.text}")
    answer = response.json()["answer"]

    # TTS
    tts_endpoint = os.environ.get("TTS_ENDPOINT")
    data = {"text": answer}
    response = requests.post(tts_endpoint, data=json.dumps(data))
    answer_speech = response.json()["speech"]

    # Convert to base64 type since base64 is more efficient for audio to transfer than bytes type
    return {"answer_text": answer, "answer_speech": answer_speech}


def lambda_handler(event, context):
    load_dotenv()

    if "body" not in event or event["httpMethod"] != "POST":
        return {"statusCode": 400, "body": json.dumps({"message": "Bad Request"})}

    if "image_file_content" in event:
        bucket_name = os.environ.get("IMAGE_BUCKET")
        with ThreadPoolExecutor as executor:
            upload_future = executor.submit(upload_image_to_S3, event["speech"], bucket_name)
            vqa_future = executor.submit(vqa_handler, event["speech"], event["image_file_content"])
        try:
            image_id = upload_future.result()
            vqa_output = vqa_future.result()
        except Exception as err:
            return {"statusCode": 500, "body": json.dumps({"message": err})}
        else:
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        "image_id": image_id,
                        "answer_text": vqa_output.get("answer_text"),
                        "answer_speech": vqa_output.get("answer_speech"),
                    }
                ),
            }
    elif "image_id" in event["body"]:
        try:
            vqa_output = vqa_handler(speech=event["speech"], image=event["body"]["image_id"])
        except Exception as err:
            return {"statusCode": 500, "body": json.dumps({"message": err})}
        else:
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        "image_id": image_id,
                        "answer_text": vqa_output.get("answer_text"),
                        "answer_speech": vqa_output.get("answer_speech"),
                    }
                ),
            }

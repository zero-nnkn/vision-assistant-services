import json
import os
import uuid

import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.environ.get("AWS_REGION", "us-west-2"),
)


def lambda_handler(event, context):
    """[AWS Lambda entrypoint]
    Contains logic of the Lambda, which processes user's feedbacks.
    Feedbacks are stored in AWS Dynamodb and later used for continual learning.

    Return:
        feedback_id: database index of the feedback
    """
    if "body" not in event or event["httpMethod"] != "POST":
        return {"statusCode": 400, "body": json.dumps({"message": "Bad Request"})}

    request_body = json.loads(event["body"])
    image_id = request_body.get("image_id")
    question = request_body.get("question")
    answer = request_body.get("answer")
    feedback = request_body.get("feedback")

    id = uuid.uuid4().hex

    try:
        table = dynamodb.Table(os.environ.get("TABLE_NAME", "feedback-table"))
        table.put_item(
            Item={
                "feedback_id": id,
                "image_id": image_id,
                "question": question,
                "answer": answer,
                "feedback": {
                    "react": feedback.get("react"),
                    "comment": feedback.get("comment"),
                },
            }
        )
    except Exception:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error"}),
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Feedback is saved successfully", "feedback_id": id}),
        }

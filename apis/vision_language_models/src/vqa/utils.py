import boto3
from botocore.exceptions import ClientError


class S3ObjectQuery:
    def __init__(self, bucket_name, aws_access_key_id, aws_secret_access_key):
        self.bucket_name = bucket_name
        self.s3 = boto3.resource(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        
    def query(self, filename):
        try:
            obj = self.s3.Object(self.bucket_name, filename)
            file_content = obj.get()["Body"].read()
        except ClientError as err:
            raise Exception(err.response["Error"]["Message"])
        else:
            return file_content

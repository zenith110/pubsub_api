import boto3
import os
from botocore.client import ClientError
"""
Checks if the bucket for the specific pull request exist. This will occur on the creation of the pull request.
If it does, returns a success and triggers a job that will init the terraform creation of the terraform state on the bucket
If it does not, create the bucket, then run the init
"""
def bucket_exist():
    s3 = boto3.resource(
        service_name="s3",
        region_name="us-east-2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        s3.meta.client.head_bucket(Bucket=os.getenv("BUCKET_NAME"))
    except ClientError:
        return ClientError
if __name__ == "__main__":
    bucket_exist()
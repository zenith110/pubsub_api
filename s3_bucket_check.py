import boto3
import os
from botocore.client import ClientError
"""
Checks if the bucket for the specific pull request exist. This will occur on the creation of the pull request.
If it does, returns a success and triggers a job that will init the terraform creation of the terraform state on the bucket
If it does not, create the bucket, then run the init
"""
s3 = boto3.resource(
    service_name="s3",
    region_name="us-east-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
bucket = s3.Bucket(os.getenv("BUCKET_NAME"))
exists = True
try:
    bucket = s3.meta.client.head_bucket(Bucket=os.getenv("BUCKET_NAME"))
    print(bucket)
except ClientError as e:
# If a client error is thrown, then check that it was a 404 error.
# If it was a 404 error, then the bucket does not exist.
    error_code = e.response['Error']['Code']
    if error_code == '404':
        exists = False
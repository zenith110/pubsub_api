import boto3
import os
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
my_bucket = s3.create_bucket(Bucket=os.getenv("BUCKET_NAME"))
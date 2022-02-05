import boto3
import os
"""
Creates a file after terraform is first initalized
"""
s3 = boto3.resource(
    service_name="s3",
    region_name="us-east-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


txt_data = b'File Created upon first creation'

object = s3.Object(os.getenv("BUCKET_NAME"), 'first.txt')

result = object.put(Body=txt_data)

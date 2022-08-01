from bucket.m_config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME, AWS_S3_BUCKET_REGION, AWS_S3_BUCKET_URL
import boto3
import uuid

def s3_upload(user, temp):
    s3 = boto3.client(
            service_name='s3',
            region_name=AWS_S3_BUCKET_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    try:
        s3.upload_file(f'{user}/{temp}', AWS_S3_BUCKET_NAME, f'video/{temp}', ExtraArgs={'ACL':'public-read'}) 
    except Exception as e:
        print(e)
        return False

    location = f'{AWS_S3_BUCKET_URL}/video/{uuid.uuid1()}.mp4'

    return location

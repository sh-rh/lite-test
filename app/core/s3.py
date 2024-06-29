from typing import Any
from collections.abc import AsyncGenerator
from aiobotocore.session import get_session
from aiobotocore.client import AioBaseClient
from fastapi import UploadFile
from botocore.exceptions import ClientError


from app.core.config import settings


config = {"aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
          "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
          "endpoint_url": settings.AWS_ENDPOIN_URL,
          "region_name": settings.AWS_REGION
          }

bucket_name = settings.S3_BUCKET


async def get_client() -> AsyncGenerator[AioBaseClient, Any, None]:
    async with get_session().create_client(service_name='s3', **config) as s3_client:
        yield s3_client


async def upload_file(s3_client: AioBaseClient, file_obj: UploadFile,):
    object_name = file_obj.filename
    try:
        file_upload_response = await s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=file_obj.file,
            StorageClass='COLD',
        )

    except ClientError as e:
        return e

    return file_upload_response

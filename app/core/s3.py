import os
from typing import Any
from collections.abc import AsyncGenerator
from aiobotocore.session import get_session
from aiobotocore.client import AioBaseClient
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


async def upload_file(s3_client: AioBaseClient, file_obj: bytes, project_id: int, filename: str) -> Any:
    object_name = filename
    try:
        file_upload_response = await s3_client.put_object(
            Bucket=bucket_name,
            Key=f'{str(project_id)}/{object_name}',
            Body=file_obj,
            StorageClass='COLD',
        )

    except ClientError as e:
        return False

    return f'{settings.AWS_ENDPOIN_URL}/{settings.S3_BUCKET}/{str(project_id)}/{object_name}'


async def get_upload_link(s3_client: AioBaseClient, filename: str):
    try:
        is_exists = await s3_client.get_object(Bucket=bucket_name, Key=filename)

    except ClientError as e:
        return False

    if is_exists:
        return f'{settings.AWS_ENDPOIN_URL}/{settings.S3_BUCKET}/{filename}'


async def get_file(s3_client: AioBaseClient, filename: str):
    try:
        response = await s3_client.get_object(Bucket=bucket_name, Key=filename)
        data = await response["Body"].read()
        return data

    except ClientError as e:
        return False

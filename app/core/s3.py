import os
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


async def upload_file(s3_client: AioBaseClient, file_obj: UploadFile) -> Any:
    object_name = file_obj.filename
    try:
        file_upload_response = await s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=file_obj.file,
            StorageClass='COLD',
        )

    except ClientError as e:
        return False

    return file_upload_response


async def get_upload_link(s3_client: AioBaseClient, filename: str):
    try:
        is_exists = await s3_client.get_object(Bucket=bucket_name, Key=filename)

    except ClientError as e:
        return False

    if is_exists:
        return f'{settings.AWS_ENDPOIN_URL}/{settings.S3_BUCKET}/{filename}'


async def get_file(s3_client: AioBaseClient, filename: str, project_id: str):
    destination_path = os.path.join(settings.PROJECTS_PATH, project_id, filename)
    try:
        response = await s3_client.get_object(Bucket=bucket_name, Key=filename)
        data = await response["Body"].read()
        with open(destination_path, "wb") as file:
            file.write(data)
    except ClientError as e:
        return False

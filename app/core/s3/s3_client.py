from typing import Any
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from fastapi import UploadFile


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
            region: str
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
            "region_name": region
        }

        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[AioBaseClient, Any]:
        async with self.session.create_client(service_name='s3', **self.config) as client:
            yield client

    async def upload_file(
            self,
            file: UploadFile,
            object_name: str
    ):
        try:
            async with self.get_client() as client:
                await client.put_object(Bucket=self.bucket_name, Key=object_name, Body=file.file)

        except ClientError as e:
            return {'msg': e}

        return True

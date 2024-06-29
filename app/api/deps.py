from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from aiobotocore.client import AioBaseClient

from app.core.db import get_session
from app.core.s3 import get_client


AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]

S3ClientDep = Annotated[AioBaseClient, Depends(get_client)]

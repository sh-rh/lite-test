import datetime
import os
from typing import Annotated, Any
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile


from app.models import ImageCreate, ImagePublic, ImagesPublic, Image, Versions, VersionsCreate
from app.api.deps import AsyncSessionDep
from app import crud
from app.core.s3.s3_client import S3Client


s3_client = S3Client(
    access_key="YCAJEhOFV72xP6zEiGrfe36Gc",
    secret_key="YCMawddAr2cQGIxuA221Sjg4IjB5xYZieIlZ9Eq2",
    endpoint_url="https://storage.yandexcloud.net",
    bucket_name="gaga",
    region='ru-central1'
)

router = APIRouter()


@router.post('/', response_model=ImagePublic)
async def create_image(*, session: AsyncSessionDep, image_in: Annotated[ImageCreate, Depends()]) -> Any:
    project = await crud.get_proj_by_id(session=session, proj_id=image_in.project_id)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    versions_in = VersionsCreate(original="надо сделать",
                                 thumb="надо сделать",
                                 big_thumb="надо сделать",
                                 big_1920="надо сделать",
                                 d2500="надо сделать")

    versions = Versions.model_validate(versions_in)

    state = 'надо сделать'

    return await crud.create_image(session=session, image=image_in, state=state, versions=versions)


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    res = await s3_client.upload_file(file, 'gaga')
    return res

from typing import Annotated, Any
from aiohttp import ClientError
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File


from app.core.config import settings
from app.core.s3 import get_upload_link, get_file, upload_file
from app.models import ImageCreate, Versions, VersionsCreate
from app.api.deps import AsyncSessionDep, S3ClientDep
from app import crud
from app.utils import image_resize

router = APIRouter()


@router.post('/')
async def create_image(*, session: AsyncSessionDep,
                       s3_client: S3ClientDep,
                       image_in: Annotated[ImageCreate, Depends()]
                       ) -> Any:
    upload_link = await get_upload_link(s3_client=s3_client, filename=image_in.filename)

    project = await crud.get_proj_by_id(session=session, proj_id=image_in.project_id)

    if upload_link is None:
        raise HTTPException(status_code=404, detail="Image not found")

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    file_path = await get_file(s3_client=s3_client, filename=image_in.filename, project_id=str(project.id))

    versions_dict = {}

    versions_dict['original'] = await image_resize(file_path)
    versions_dict['thumb'] = await image_resize(file_path, 150, 120)
    versions_dict['big_thumb'] = await image_resize(file_path, 700, 700)
    versions_dict['big_1920'] = await image_resize(file_path, 1920, 1080)
    versions_dict['d2500'] = await image_resize(file_path, 2500, 2500)

    versions_in = VersionsCreate(**versions_dict)

    versions = Versions.model_validate(versions_in)

    state = 'надо сделать'

    await crud.create_image(session=session, image=image_in, state=state, versions=versions)

    return {'upload_link': upload_link, 'params': {}}


@router.post('/upload')
async def upload_image(*, s3_client: S3ClientDep, file_obj: UploadFile = File(...)):
    upload_link = await upload_file(s3_client=s3_client, file_obj=file_obj.file, project_id=1, filename=file_obj.filename)
    return {'upload_link': upload_link}


@router.get('/bucket')
async def bucket_list(*, s3_client: S3ClientDep):
    res = []
    try:
        objects = (await s3_client.list_objects(Bucket=settings.S3_BUCKET))['Contents']
        for key in objects:
            res.append(key)
    except KeyError as e:
        raise HTTPException(status_code=400, detail="Empty.")
    return res


@router.get('/resize')
async def resize(*, session: AsyncSessionDep,
                 s3_client: S3ClientDep):
    file_origen = await get_file(s3_client=s3_client, filename='girl.jpg')
    file_resized = (await image_resize(file_origen, 500, 500))
    upload_link = await upload_file(s3_client=s3_client, file_obj=file_resized, project_id=1, filename='resized_girl.jpg')
    return upload_link

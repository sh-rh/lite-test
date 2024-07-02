from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException


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

    if upload_link is None:
        raise HTTPException(status_code=404, detail="Image not found")

    project = await crud.get_proj_by_id(session=session, proj_id=image_in.project_id)

    if project is None:
        project = await crud.create_project(session=session, proj_id=image_in.project_id)

    file_data = await get_file(s3_client=s3_client, filename=image_in.filename)

    versions_dict = {}

    versions_dict['original'] = await upload_file(s3_client=s3_client,
                                                  file_obj=await image_resize(
                                                      file_data),
                                                  project_id=image_in.project_id,
                                                  filename=image_in.filename)

    versions_dict['thumb'] = await upload_file(s3_client=s3_client,
                                               file_obj=await image_resize(
                                                   file_data, width=150, height=120), project_id=image_in.project_id,
                                               filename=f'{image_in.filename.split('.')[0]}_thumb_{image_in.filename.split('.')[1]}')

    versions_dict['big_thumb'] = await upload_file(s3_client=s3_client,
                                                   file_obj=await image_resize(
                                                       file_data, width=700, height=700), project_id=image_in.project_id, filename=f'{image_in.filename.split('.')[0]}_big_thumb_{image_in.filename.split('.')[1]}')

    versions_dict['big_1920'] = await upload_file(s3_client=s3_client,
                                                  file_obj=await image_resize(
                                                      file_data, width=1920, height=1080), project_id=image_in.project_id, filename=f'{image_in.filename.split('.')[0]}_big_1920_{image_in.filename.split('.')[1]}')

    versions_dict['d2500'] = await upload_file(s3_client=s3_client,
                                               file_obj=await image_resize(
                                                   file_data, width=2500, height=2500),
                                               project_id=image_in.project_id,
                                               filename=f'{image_in.filename.split('.')[0]}_d2500_{image_in.filename.split('.')[1]}')

    versions_in = VersionsCreate(**versions_dict)

    versions = Versions.model_validate(versions_in)

    state = 'uploud'

    await crud.create_image(session=session, image=image_in, state=state, versions=versions)

    return {'upload_link': upload_link, 'params': {}}

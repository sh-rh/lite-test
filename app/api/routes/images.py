from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException


from app.core.s3 import get_upload_link, get_file
from app.models import ImageCreate, ImagePublic, Versions, VersionsCreate
from app.api.deps import AsyncSessionDep, S3ClientDep
from app import crud

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

    await get_file(s3_client=s3_client, filename=image_in.filename, project_id=str(project.id))

    versions_in = VersionsCreate(original=f'{image_in.filename}',
                                 thumb="надо сделать",
                                 big_thumb="надо сделать",
                                 big_1920="надо сделать",
                                 d2500="надо сделать")

    versions = Versions.model_validate(versions_in)

    state = 'надо сделать'

    await crud.create_image(session=session, image=image_in, state=state, versions=versions)

    return {'upload_link': upload_link, 'params': {}}

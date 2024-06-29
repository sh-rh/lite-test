from typing import Annotated, Any
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile


from app.core.s3 import upload_file
from app.models import ImageCreate, ImagePublic, Versions, VersionsCreate
from app.api.deps import AsyncSessionDep, S3ClientDep
from app import crud

router = APIRouter()


@router.post('/', response_model=ImagePublic)
async def create_image(*, session: AsyncSessionDep,
                       s3_client: S3ClientDep,
                       image_in: Annotated[ImageCreate, Depends()],
                       file_obj: UploadFile = File(...)) -> Any:
    project = await crud.get_proj_by_id(session=session, proj_id=image_in.project_id)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    await upload_file(s3_client=s3_client, file_obj=file_obj)

    versions_in = VersionsCreate(original=f'{file_obj.filename}',
                                 thumb="надо сделать",
                                 big_thumb="надо сделать",
                                 big_1920="надо сделать",
                                 d2500="надо сделать")

    versions = Versions.model_validate(versions_in)

    state = 'надо сделать'

    return await crud.create_image(session=session, image=image_in, state=state, versions=versions)

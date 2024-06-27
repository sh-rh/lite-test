from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException


from app.models import ImageCreate, ImagePublic, ImagesPublic, Image, VersionsCreate
from app.api.deps import SessionDep
from app import crud

router = APIRouter()


@router.post('/', response_model=ImagePublic)
async def create_image(*, session: SessionDep, image_in: Annotated[ImageCreate, Depends()]) -> ImagePublic:
    project = await crud.get_proj_by_id(session=session, proj_id=image_in.project_id)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    versions = {
        "original": "надо сделать",
        "thumb": "надо сделать",
        "big_thumb": "надо сделать",
        "big_1920": "надо сделать",
        "d2500": "надо сделать"
    }

    image = Image.model_validate(
        image_in, update={'state': 'надо сделать', 'versions': versions})

    return await crud.create_image(session=session, image=image)

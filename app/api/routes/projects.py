from typing import Annotated, Any
from fastapi import APIRouter, Depends


from app.models import ProjectPublic, ProjectsPublic, ProjectCreate, ImagesPublic
from app.api.deps import SessionDep
from app import crud

router = APIRouter()


@router.get('/', response_model=ProjectsPublic)
async def read_projects(session: SessionDep) -> Any:
    return await crud.get_projects(session=session)


@router.get('/{id}/images', response_model=ImagesPublic)
async def read_images(session: SessionDep, id: int) -> Any:
    return await crud.get_images(session=session, proj_id=id)

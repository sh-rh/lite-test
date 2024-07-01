from typing import Any
from fastapi import APIRouter, HTTPException


from app.models import Project, ProjectCreate, ProjectPublic, ProjectsPublic, ImagesPublic
from app.api.deps import AsyncSessionDep
from app import crud

router = APIRouter()


@router.get('/', response_model=ProjectsPublic)
async def read_projects(session: AsyncSessionDep) -> Any:
    projects = await crud.get_projects(session=session)

    if projects is None:
        raise HTTPException(status_code=404, detail="Projects not found")

    return projects


@router.get('/{project_id}/images', response_model=ImagesPublic)
async def read_project_images(session: AsyncSessionDep, project_id: int) -> Any:
    images = await crud.get_images(session=session, proj_id=project_id)

    if images is None:
        raise HTTPException(status_code=400, detail="Something went wrong")

    return images

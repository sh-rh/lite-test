from typing import Any
from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Image, \
    ImageCreate, \
    ImagesPublic, \
    Project, \
    ProjectCreate, ProjectPublic, \
    ProjectsPublic, Versions, \
    VersionsCreate


async def create_project(*, session: AsyncSession) -> Project:
    db_obj = Project()

    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)

    return db_obj


async def create_image(*, session: AsyncSession,
                       image: ImageCreate,
                       state: str,
                       versions: Versions
                       ) -> Image:

    db_obj = Image.model_validate(
        image, update={'state': state, 'versions': versions})

    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)

    return db_obj


async def get_projects(*, session: AsyncSession) -> Any:
    projects = await session.exec(select(Project))
    return ProjectsPublic(projects=projects)


async def get_proj_by_id(*, session: AsyncSession, proj_id: int) -> Any:
    project = (await session.exec(select(Project).where(Project.id == proj_id))).first()

    if not project:
        return None

    return project


async def get_images(*, session: AsyncSession, proj_id: int) -> Any:
    images = (await session.exec(select(Project).where(Project.id == proj_id))).first().images

    return ImagesPublic(images=images)

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Image, ImageCreate, ImagesPublic, Project, ProjectCreate, ProjectsPublic


async def create_project(*, session: AsyncSession, project_create: ProjectCreate) -> Project:
    db_obj = Project.model_validate(project_create)

    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)

    return db_obj


async def create_image(*, session: AsyncSession, image: ImageCreate, state: str) -> Image:
    db_obj = Image.model_validate(image, state=state)

    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)

    return db_obj


async def get_projects(*, session: AsyncSession) -> ProjectsPublic:
    projects = await session.exec(select(Project))
    return ProjectsPublic(projects=projects)


async def get_images(*, session: AsyncSession, proj_id: int) -> ImagesPublic:
    project = select(Project).where(Project.id == proj_id)
    images = await session.exec(project)

    return ImagesPublic(images=images)

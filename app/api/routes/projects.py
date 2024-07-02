from typing import Any
from fastapi import APIRouter, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.models import ImagesPublic
from app.api.deps import AsyncSessionDep
from app import crud
from app.utils import ConnectionManager

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'view')))

manager = ConnectionManager()


@router.get('/')
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


@router.get('/status')
async def get_status_page(request: Request):
    return templates.TemplateResponse(name='status.html',
                                      context={'request': request,
                                               'title': f"Project status."})


@router.websocket('/ws/{client_id}')
async def websocket_endpoint(session: AsyncSessionDep, websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            project_id = int(await websocket.receive_text())
            await manager.send_personal_message(f"{project_id}'s project status", websocket)

            project = await crud.get_proj_by_id(proj_id=project_id, session=session)
            if project is None:
                await manager.send_personal_message(f"Projects not found", websocket)

            project_images = await crud.get_images(session=session, proj_id=project_id)

            for image in project_images.model_dump()['images']:
                await manager.send_personal_message(f"image with id {image['id']} is {image['state']}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

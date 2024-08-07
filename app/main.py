from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI
from app.core.db import init_db
from app.api.routes import projects, images


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(projects.router, prefix='/projects', tags=['projects'])
app.include_router(images.router, prefix='/images', tags=['images'])

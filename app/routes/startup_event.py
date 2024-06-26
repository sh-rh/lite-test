from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from sqlmodel import SQLModel, Session

from ..db import engine, init_db

router = APIRouter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    with Session(engine) as session:
        init_db(session)
    yield

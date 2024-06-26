from fastapi import FastAPI

from app.routes.startup_event import lifespan


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {'foo': 'bar gagaa'}

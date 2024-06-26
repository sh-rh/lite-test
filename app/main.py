from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def foo():
    return {'foo': 'bar gagag'}

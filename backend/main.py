from fastapi import FastAPI
from .routers import tasks

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}


app.include_router(tasks.router)
from fastapi import FastAPI
from .routers import todos

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}


app.include_router(todos.router)
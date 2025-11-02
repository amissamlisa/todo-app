from fastapi import FastAPI
from .routers import goal_tasks, auth

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}

app.include_router(goal_tasks.router)
app.include_router(auth.router)
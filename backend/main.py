from fastapi import FastAPI
from .routers import goal_tasks, auth, goal

app = FastAPI()

app.include_router(goal_tasks.router)
app.include_router(auth.router)
app.include_router(goal.router)
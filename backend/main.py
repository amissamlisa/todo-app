from fastapi import FastAPI
from .routers import goal_tasks, auth, goal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)
app.include_router(goal_tasks.router)
app.include_router(auth.router)
app.include_router(goal.router)
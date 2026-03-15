from fastapi import FastAPI

from backend.exceptions.app_exception import AppException
from backend.routers import top
from .routers import goal_tasks, auth, goal
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from starlette.exceptions import HTTPException 
from fastapi.exceptions import RequestValidationError
from backend.exception_handler import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

app = FastAPI()

origins = [
    settings.ALLOWED_ORIGIN_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
app.include_router(goal_tasks.router)
app.include_router(auth.router)
app.include_router(goal.router)
app.include_router(top.router)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
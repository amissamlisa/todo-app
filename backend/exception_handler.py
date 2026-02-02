from typing import Any
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from backend.exceptions.app_exception import AppException
from backend.utils.parse import parse_validation_errors

def generate_error_response(
    status_code: int,
    error_code: str,
    message: str,
    error: Any = None,
    headers: dict | None = None,
):
    return JSONResponse(
        status_code=status_code,
        headers=headers,
        content={
            "error_code": error_code,
            "message": message,
            "error": error,
        },
    )

# HTTPException 用
def http_exception_handler(request: Request, exc: HTTPException):
    return generate_error_response(
        status_code=exc.status_code,
        error_code="HTTP_ERROR",
        message="HTTP Exception",
        error=exc.detail
    )
# カスタムエラー用
def app_exception_handler(request: Request, exc: AppException):
    return generate_error_response(
        status_code=exc.status_code,
        headers=exc.headers,
        error_code=exc.error_code,
        message=exc.error_message,
        error=exc.error
    )

# バリデーションエラー用
def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = parse_validation_errors(exc.errors())
    return generate_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_code="VALIDATION_ERROR",
        message="Validation Error",
        error=errors
    )

# 想定外エラー用
def generic_exception_handler(request: Request, exc: Exception):
    return generate_error_response(
        status_code=500,
        error_code="INTERNAL_ERROR",
        message="Internal Server Error",
        error=str(exc)
    )
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

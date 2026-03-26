"""Custom exception hierarchy and FastAPI exception handlers.

This module ensures error responses follow the same envelope as
`app.core.response_formatter`.
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.response_formatter import error_response


# ── Custom exception hierarchy ────────────────────────────────────────────────

class AppException(Exception):
    """
    Base class for all application-level exceptions.

    Subclass it and set `status_code` / `detail` as class attributes, or
    pass them at raise-time for a one-off message.
    """

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "An unexpected error occurred."

    def __init__(
        self,
        detail: str | None = None,
        status_code: int | None = None,
    ) -> None:
        self.detail = detail or self.__class__.detail
        self.status_code = status_code or self.__class__.status_code
        super().__init__(self.detail)


class NotFoundException(AppException):
    """HTTP 404 — requested resource does not exist."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found."


class ConflictException(AppException):
    """HTTP 409 — resource already exists / unique constraint violation."""

    status_code = status.HTTP_409_CONFLICT
    detail = "Resource already exists."


class BadRequestException(AppException):
    """HTTP 400 — invalid input that passes schema validation but is logically wrong."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Bad request."


class UnauthorizedException(AppException):
    """HTTP 401 — missing or invalid authentication credentials."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentication required."


class ForbiddenException(AppException):
    """HTTP 403 — authenticated but not permitted."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "You do not have permission to perform this action."


class ServiceUnavailableException(AppException):
    """HTTP 503 — downstream service (e.g. database) temporarily unavailable."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    detail = "Service temporarily unavailable. Please try again later."


# ── Exception handlers ────────────────────────────────────────────────────────

async def _app_exception_handler(
    request: Request,  # noqa: ARG001
    exc: AppException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
<<<<<<< HEAD:app/exceptions.py
        content={
            "success": False,
            "message": exc.detail,
            "data": None,
            "code": exc.status_code,
        },
=======
        content=error_response(message=exc.detail, code=exc.status_code, data=None),
    )


async def _validation_exception_handler(
    request: Request,  # noqa: ARG001
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            message="Validation error",
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            data={"errors": exc.errors()},
        ),
    )


async def _http_exception_handler(
    request: Request,  # noqa: ARG001
    exc: StarletteHTTPException,
) -> JSONResponse:
    # FastAPI/Starlette raise these for things like 404/405 and explicit HTTPException.
    detail = exc.detail if isinstance(exc.detail, str) else "HTTP error"
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=detail, code=exc.status_code, data=None),
>>>>>>> 7199041aea298502b86585a00da5e2a710d75cd3:app/core/exceptions.py
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Attach all custom exception handlers to the given FastAPI instance."""
    app.add_exception_handler(AppException, _app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, _validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, _http_exception_handler)  # type: ignore[arg-type]

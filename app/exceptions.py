"""
Custom exception hierarchy and FastAPI exception handlers.

Usage in a route:
    from app.exceptions import NotFoundException
    raise NotFoundException("User 42 not found.")

Register all handlers once in create_app():
    from app.exceptions import register_exception_handlers
    register_exception_handlers(app)
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


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
        content={"detail": exc.detail},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Attach all custom exception handlers to the given FastAPI instance."""
    app.add_exception_handler(AppException, _app_exception_handler)  # type: ignore[arg-type]

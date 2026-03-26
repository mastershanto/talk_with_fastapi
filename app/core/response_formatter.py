"""
Response formatting utilities for consistent API response envelopes.

All responses follow the standard format:
    {
        "success": bool,
        "message": str,
        "data": Any,
        "code": int
    }
"""

from typing import Any


def success_response(
    data: Any = None,
    message: str = "Success",
    code: int = 200,
) -> dict:
    """
    Create a standard success response.

    Args:
        data: Response payload (list, dict, object, etc.)
        message: Human-readable success message
        code: HTTP status code

    Returns:
        Standard response envelope dict

    Example:
        return success_response(
            data=user_dict,
            message="User created successfully",
            code=201
        )
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "code": code,
    }


def list_response(
    items: list,
    message: str = "Success",
    code: int = 200,
) -> dict:
    """
    Create a response for list endpoints.

    Args:
        items: List of items
        message: Human-readable message
        code: HTTP status code

    Returns:
        Standard response envelope dict
    """
    return success_response(
        data=items,
        message=message,
        code=code,
    )


def error_response(
    message: str,
    code: int = 400,
    data: Any = None,
) -> dict:
    """
    Create a standard error response.

    Args:
        message: Error message
        code: HTTP status code
        data: Optional additional error details

    Returns:
        Standard response envelope dict
    """
    return {
        "success": False,
        "message": message,
        "data": data,
        "code": code,
    }

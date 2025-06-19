"""Wrapper for API Error Responses."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from core.errcode import CustomErrorCode

if TYPE_CHECKING:
    from ninja.errors import ValidationError


class CustomError(Exception):
    def __init__(self, status_code: int, error_code: str, message: Any):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message


class UnauthenticatedError(CustomError):
    """Handle unauthenticated request."""

    def __init__(self, error_code, message):
        self.status_code = 401
        self.error_code = error_code
        self.message = message


class UnauthorizedError(CustomError):
    """Handle unauthorized request."""

    def __init__(self, error_code, message):
        self.status_code = 403
        self.error_code = error_code
        self.message = message


class ConflictError(CustomError):
    """Resource conflict error."""

    def __init__(self, error_code, message):
        self.status_code = 409
        self.error_code = error_code
        self.message = message


class NotFoundError(CustomError):
    """Resource not found error."""

    def __init__(self, error_code, message):
        self.status_code = 404
        self.error_code = error_code
        self.message = message


class BadRequestError(CustomError):
    """Handle bad request."""

    def __init__(self, error_code, message):
        self.status_code = 400
        self.error_code = error_code
        self.message = message


class InternalServerError(CustomError):
    """Internal server error exception."""

    def __init__(self, error_code, message):
        self.status_code = 500
        self.error_code = error_code
        self.message = message


class ValidationErrorDetail(BaseModel):
    """Details of an API validation error."""

    location: str
    message: str
    error_type: str
    context: dict[str, Any] | None = None


class APIValidationError(BaseModel):
    """Wrapper for API validation errors."""

    error_code: str = CustomErrorCode.VALIDATE_ERROR
    message: str
    errors: list[ValidationErrorDetail]

    @classmethod
    def from_pydantic(cls, exc: ValidationError) -> APIValidationError:
        """Create an APIValidationError instance from a Pydantic ValidationError."""
        return cls(
            error_code=CustomErrorCode.VALIDATE_ERROR,
            message="Pydanyic Validation Errors",
            errors=[
                ValidationErrorDetail(
                    location=" -> ".join(map(str, err["loc"])),
                    message=err["msg"],
                    error_type=err["type"],
                    context=err.get("ctx"),
                )
                for err in exc.errors  # iterate over each error in the Pydantic ValidationError
            ],
        )

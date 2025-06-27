import jwt
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError

from .errcode import CustomErrorCode
from .exceptions import APIValidationError, CustomError

api = NinjaAPI()

api.add_router(prefix="/users/", router="account.api.router", tags=["users"])
api.add_router(prefix="/auth/", router="auth.api.router", tags=["auth"])


@api.exception_handler(CustomError)
def custom_error_handler(request: HttpRequest, exc: CustomError) -> HttpResponse:
    """Handle custom error."""
    return api.create_response(
        request,
        data={"error_code": exc.error_code, "message": exc.message},
        status=exc.status_code,
    )


@api.exception_handler(exc_class=ValidationError)
def validation_exception_handler(request: HttpRequest, exc: ValidationError) -> HttpResponse:
    """Handle validation exceptions."""
    return api.create_response(
        request,
        data=APIValidationError.from_pydantic(exc).model_dump(exclude_none=True),
        status=400,
    )


@api.exception_handler(jwt.exceptions.PyJWTError)
def jwt_exception_handler(request: HttpRequest, exc: jwt.exceptions.PyJWTError) -> HttpResponse:
    """Handle exceptions related to JWT authentication errors."""
    if isinstance(exc, jwt.exceptions.ExpiredSignatureError):
        return api.create_response(
            request,
            data={"error_code": CustomErrorCode.TOKEN_EXPIRED, "message": "Token expired"},
            status=401,
        )
    return api.create_response(
        request,
        data={"error_code": CustomErrorCode.INVALID_CREDENTIALS, "message": "Could not validate credentials"},
        status=401,
    )

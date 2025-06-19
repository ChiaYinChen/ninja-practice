from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError

from .exceptions import APIValidationError, CustomError

api = NinjaAPI()

api.add_router(prefix="/users/", router="account.api.router", tags=["users"])


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

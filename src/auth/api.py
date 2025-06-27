from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.http import HttpRequest
from ninja import Router

from core import exceptions as exc
from core.errcode import CustomErrorCode
from core.responses import GenericResponse

from .schemas import LoginRequest, Token
from .security import create_access_token, create_refresh_token

router = Router()


@router.post(
    "/login",
    response=GenericResponse[Token],
    summary="Authenticate user and generate tokens",
)
def login(request: HttpRequest, login_data: LoginRequest):
    """
    Authenticate a user via email and password, then generate access and refresh tokens.

    * access token expires in 15 minutes
    * refresh token expires in 24 hours
    """
    user = authenticate(email=login_data.email, password=login_data.password)
    if not user:
        raise exc.UnauthenticatedError(CustomErrorCode.INCORRECT_EMAIL_OR_PASSWORD, "Incorrect email or password")
    update_last_login(None, user)
    return GenericResponse(
        data={
            "access_token": create_access_token(sub=user.email),
            "refresh_token": create_refresh_token(sub=user.email),
            "token_type": "bearer",
        }
    )

from django.http import HttpRequest
from ninja.security import HttpBearer

from account.models import User
from core import exceptions as exc
from core.errcode import CustomErrorCode

from .schemas import TokenPayload
from .security import decode_token


class TokenBearer(HttpBearer):
    """Handle token authentication using HTTP Bearer token."""

    def __call__(self, request: HttpRequest) -> TokenPayload:
        auth = request.headers.get(self.header)
        if not auth:
            raise exc.UnauthenticatedError(CustomErrorCode.NOT_AUTHENTICATED, "Not authenticated")
        if not auth.startswith("Bearer "):
            raise exc.UnauthenticatedError(CustomErrorCode.INVALID_CREDENTIALS, "Malformed authorization header")

        token = auth.split(" ", 1)[1]
        return self.authenticate(request, token)

    def authenticate(self, request: HttpRequest, token: str) -> User:
        token_data = decode_token(token=token)
        if not self.validate_token_data(token_data):
            raise exc.UnauthenticatedError(CustomErrorCode.INVALID_TOKEN_TYPE, "Invalid token type")
        user_obj = User.objects.filter(email=token_data.sub).first()
        if not user_obj:
            raise exc.NotFoundError(CustomErrorCode.ENTITY_NOT_FOUND, "User not found")
        return user_obj

    def validate_token_data(self, token_data: TokenPayload) -> bool:
        """Validate the token type."""
        raise NotImplementedError("Subclasses must implement this method")


class AccessTokenBearer(TokenBearer):
    """Handle access token validation."""

    def validate_token_data(self, token_data: TokenPayload) -> bool:
        """Check if the token is an access token."""
        return True if token_data.type == "access" else False

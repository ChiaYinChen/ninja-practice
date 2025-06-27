from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt

from core.config import settings

from .schemas import TokenPayload


def encode_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    """Generate a JWT token."""
    utc_now = datetime.now(UTC)
    payload = {"type": token_type, "iat": utc_now, "exp": utc_now + lifetime, "sub": str(sub), "jti": str(uuid4())}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> TokenPayload:
    """Decode a JWT token."""
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return TokenPayload(**payload)


def create_access_token(sub: str) -> str:
    """Create a short-lived access token."""
    return encode_token(
        token_type="access",
        lifetime=timedelta(seconds=settings.ACCESS_TOKEN_TTL),
        sub=sub,
    )


def create_refresh_token(sub: str) -> str:
    """Create a long-lived refresh token."""
    return encode_token(
        token_type="refresh",
        lifetime=timedelta(seconds=settings.REFRESH_TOKEN_TTL),
        sub=sub,
    )

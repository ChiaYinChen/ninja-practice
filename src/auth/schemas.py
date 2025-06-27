from ninja import Field, Schema


class LoginRequest(Schema):
    """Input schema for login request."""

    email: str = Field(examples=["user@example.com"])
    password: str


class Token(Schema):
    """Schema for token response."""

    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(Schema):
    sub: str
    type: str
    exp: int
    jti: str

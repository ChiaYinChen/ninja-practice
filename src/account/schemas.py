import re
from typing import Self

from django.conf import settings
from ninja import Field, Schema
from pydantic import field_validator, model_validator

from core import exceptions as exc
from core.errcode import CustomErrorCode


class CreateUserRequest(Schema):
    email: str = Field(examples=["user@example.com"])
    password: str = Field(min_length=8, examples=["password2025"])
    confirm_password: str = Field(min_length=8, examples=["password2025"])

    @field_validator("password")
    @classmethod
    def validate_password_contains_number(cls, v: str) -> str:
        if not re.search(r"\d", v):
            raise exc.BadRequestError(
                CustomErrorCode.VALIDATE_ERROR, "Password must contain at least one numeric character"
            )
        return v

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise exc.BadRequestError(CustomErrorCode.CONFIRM_PASSWORD_MISMATCH, "Passwords do not match")
        return self


class UserOut(Schema):
    id: int
    email: str
    created_at: str
    updated_at: str

    @staticmethod
    def resolve_created_at(instance) -> str:
        return instance.created_at.strftime(settings.DATE_TIME_FORMAT)

    @staticmethod
    def resolve_updated_at(instance) -> str:
        return instance.updated_at.strftime(settings.DATE_TIME_FORMAT)

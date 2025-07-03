from functools import wraps

from django.http import HttpRequest

from account.models import User
from core import exceptions as exc
from core.errcode import CustomErrorCode


class IsSuperUser:
    def __init__(self, request: HttpRequest, user: User) -> None:
        self.request = request
        self.user = user

    def has_permissions(self) -> bool:
        if self.user.is_superuser:
            return True
        return False


def permission_required(permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            user = getattr(request, "auth")
            permission_granted = any([permission(request, user).has_permissions() for permission in permissions])
            if not permission_granted:
                raise exc.UnauthorizedError(CustomErrorCode.OPERATION_NOT_PERMITTED, "Operation not permitted")
            return func(request, *args, **kwargs)

        return wrapper

    return decorator

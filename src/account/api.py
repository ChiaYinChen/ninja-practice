from django.http import HttpRequest
from ninja import Query, Router

from core import exceptions as exc
from core.errcode import CustomErrorCode
from core.paginations import PaginationParams, get_paginated_response
from core.responses import GenericResponse

from .models import User
from .schemas import CreateUserRequest, UserOut

router = Router()


@router.get(
    "",
    response=GenericResponse[list[UserOut]],
    summary="取得使用者清單",
)
def get_users(request: HttpRequest, paging: Query[PaginationParams]):
    user_objs = User.objects.all()
    page_info, users = get_paginated_response(user_objs, paging_params=paging)
    return GenericResponse(data=users, paging=page_info)


@router.post(
    "",
    response=GenericResponse[UserOut],
    summary="新增使用者",
)
def create_user(request: HttpRequest, payload: CreateUserRequest):
    user_obj = User.objects.filter(email=payload.email).first()
    if user_obj:
        raise exc.ConflictError(CustomErrorCode.ENTITY_CONFLICT, "Email already registered")
    user = User.objects.create_user(**payload.model_dump(exclude={"confirm_password"}))
    return GenericResponse(data=user)

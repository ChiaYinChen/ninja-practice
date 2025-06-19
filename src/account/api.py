from django.http import HttpRequest
from ninja import Router

from core.responses import GenericResponse

from .models import User
from .schemas import CreateUserRequest, UserOut

router = Router()


@router.get(
    "",
    response=GenericResponse[list[UserOut]],
    summary="取得使用者清單",
)
def get_users(request: HttpRequest):
    users = User.objects.all()
    return GenericResponse(data=users)


@router.post(
    "",
    response=GenericResponse[UserOut],
    summary="新增使用者",
)
def create_user(request: HttpRequest, payload: CreateUserRequest):
    user = User.objects.create_user(**payload.model_dump(exclude={"confirm_password"}))
    return GenericResponse(data=user)

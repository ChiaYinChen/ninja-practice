from ninja import NinjaAPI

api = NinjaAPI()

api.add_router(prefix="/users/", router="account.api.router", tags=["users"])

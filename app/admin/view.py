from sqladmin import ModelView

from app.reduction.models import ShortenModel
from app.users.models import UsersModel


class UserAdmin(ModelView, model=UsersModel):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    can_delete = False
    column_list = [UsersModel.id, UsersModel.email, UsersModel.created_at]
    column_details_exclude_list = [UsersModel.password]


class ShortenAdmin(ModelView, model=ShortenModel):
    name = "Url"
    name_plural = "Urls"
    icon = "fa-solid fa-share-nodes"
    column_list = "__all__"

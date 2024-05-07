from typing import Any, Union, Optional
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest


class EmailBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, username: Union[str, None], password: Union[str, None], **kwargs: Any) -> AbstractBaseUser | None:
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

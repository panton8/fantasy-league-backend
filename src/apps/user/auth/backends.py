from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend as ModelBackendBase

UserModel = get_user_model()


class ModelBackend(ModelBackendBase):
    def authenticate(self, request, username=None, password=None, **kwargs):
        username_field = UserModel.USERNAME_FIELD
        if kwargs.get('email') is not None:
            username_field = 'email'
            username = kwargs.get(username_field)

        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get(**{username_field: username})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            is_correct = user.check_password(password) \
                if user.has_usable_password() else user.check_md5_password(password)

            if is_correct and self.user_can_authenticate(user):
                return user

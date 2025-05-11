import hashlib
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    UserManager as BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.django_model.mixins import CreatedUpdatedAt

__all__ = (
    'User',
    'UserManager',
    'StaffUser',
)


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, CreatedUpdatedAt):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        unique=True,
        max_length=50,
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        }
    )
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    deleted_at = models.DateTimeField(_('Deleted at'), null=True, blank=True)
    md5_password = models.CharField(_('md5 password'), max_length=32, null=True, blank=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return f'User: {self.username}'

    def make_md5_password(self, raw_password: str) -> str:
        return hashlib.md5(raw_password.encode()).hexdigest()

    @staticmethod
    def is_username_in_use(username: str) -> bool:
        return User.objects.filter(username=username, is_active=True).exists()


class StaffUser(User):
    """
    This class created to work with staff users via Admin Panel
    """

    class Meta:
        proxy = True
        verbose_name = _('Staff user')
        verbose_name_plural = _('Staff users')
        permissions = (
            ('extended_session_age', 'Extended session age'),
        )

    def __str__(self):
        return f'User: {self.username}'

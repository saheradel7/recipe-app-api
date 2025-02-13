from django.db import models  # noqa

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("email is required")
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        superuser = self.create_user(
            email=self.normalize_email(email), password=password, **kwargs
        )
        superuser.is_superuser = True
        superuser.is_staff = True

        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

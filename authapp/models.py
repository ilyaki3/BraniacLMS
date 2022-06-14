from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    username = models.CharField(_("username"), max_length=150, unique=True,
                                validators=[username_validator],
                                error_messages={
                                    "unique": _("A user with that username already exists."),
                                },
                                )

    email = models.EmailField(verbose_name='Email', unique=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Возраст')
    avatar = models.ImageField(upload_to='users', blank=True, null=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

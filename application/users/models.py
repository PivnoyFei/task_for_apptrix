from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from pytils.translit import slugify

from core.fields import WEBPField
from core.models import ThumbnailMixin
from core.validators import validate_image
from users.managers import CustomUserManager


def get_upload_path(self, filename):
    return f'users/{slugify(self.last_name)}/{filename}'


class CustomUser(AbstractBaseUser, PermissionsMixin, ThumbnailMixin):
    GENDERS = (
        ("m", "Мужчина"),
        ("f", "Женщина"),
    )

    first_name = models.CharField(
        'имя',
        max_length=256,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=256,
    )
    gender = models.CharField("Пол", max_length=1, choices=GENDERS)
    email = models.EmailField(
        'почтовый адрес',
        unique=True,
    )
    _image = WEBPField(
        'аватарка',
        upload_to=get_upload_path,
        blank=True,
        null=True,
        validators=[
            validate_image,
        ],
    )
    is_staff = models.BooleanField(
        'редактор',
        default=False,
        help_text='доступно редактирование некоторых материалов на сайте.',
    )
    is_superuser = models.BooleanField(
        'администратор',
        default=False,
        help_text='делегирует полный обьем прав.',
    )
    is_active = models.BooleanField(
        'активная учетная запись',
        default=True,
        help_text='активация/деактивация учетной записи.',
    )

    @property
    def first_last_name(self):
        return f'{self.first_name} {self.last_name}'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
    ]
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_thumbnail(self, size, image):
        return self._get_thumbnail(size, self._image)

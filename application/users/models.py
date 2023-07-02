from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from pytils.translit import slugify

from core.fields import WEBPField
from core.models import ThumbnailMixin, Timestamps
from core.services import image_watermark
from core.validators import validate_image
from users.managers import CustomUserManager


def get_upload_path(self, filename):
    return f'users/{slugify(self.last_name)}/{filename}'


class CustomUser(AbstractBaseUser, PermissionsMixin, ThumbnailMixin):
    GENDERS = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    )
    first_name = models.CharField(
        'имя',
        max_length=256,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=256,
    )
    gender = models.CharField(
        'пол',
        max_length=1,
        choices=GENDERS,
    )
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

    def get_thumbnail(self, size):
        return self._get_thumbnail(size, self._image)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        super().save(*args, **kwargs)
        if not self._image:
            return
        image = image_watermark(self._image.path)
        image.save(self._image.path)


class Match(Timestamps):
    LIKE = (
        ('NA', 'Нет ответа'),
        ('OK', 'Взаимно!'),
        ('NO', 'Не взаимно'),
    )
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sender',
        verbose_name='отправитель',
    )
    receiver = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='receiver',
        verbose_name='получатель',
    )
    is_sympathy = models.CharField(
        'взаимная симпатия',
        max_length=2,
        choices=LIKE,
        default='NA',
    )

    class Meta:
        verbose_name = 'взаимная симпатия'
        verbose_name_plural = 'взаимные симпатии'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'sender',
                    'receiver',
                ),
                name='unique_match',
            ),
        )

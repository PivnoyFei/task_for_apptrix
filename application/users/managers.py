from decimal import Decimal

from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Case, Prefetch, When
from django.db.models.functions import Radians

from core.services import get_sql_distance


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        is_staff = kwargs.pop('is_staff', False)
        is_superuser = kwargs.pop('is_superuser', False)
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        return self._create_user(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )

    def match(self, user_sender, user_receiver):
        sender = Prefetch(
            'sender',
            apps.get_model('users', 'Match')
            .objects.only('id', 'is_sympathy')
            .filter(receiver=user_receiver),
            to_attr='user_sender',
        )
        return (
            self.filter(id=user_sender, is_active=True)
            .prefetch_related(sender)
            .only('id', 'first_name', 'email')
            .first()
        )

    def cactom(self, user):
        longitude = Radians(user.longitude)
        latitude = Radians(user.latitude)
        distance = get_sql_distance(longitude, latitude)

        return self.annotate(
            distance=Case(When(longitude=None, then=Decimal('0')), default=distance)
        ).only(
            'id',
            'first_name',
            'last_name',
            'gender',
            'email',
            '_image',
            'latitude',
            'longitude',
        )

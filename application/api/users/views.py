from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from api.users.serializers import UserCreateSerializer


class UserCreateViewSet(GenericViewSet, CreateModelMixin):
    http_method_names = ['post']
    serializer_class = UserCreateSerializer

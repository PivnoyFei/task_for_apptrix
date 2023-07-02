from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.users.filters import UserFilter
from api.users.serializers import UserCreateSerializer, UserSerializer
from core.services import get_distance, match_send_mail
from users.models import CustomUser, Match


class UserCreateViewSet(GenericViewSet, CreateModelMixin):
    http_method_names = ['post']
    serializer_class = UserCreateSerializer


class MatchViewSet(RetrieveModelMixin, GenericViewSet):
    http_method_names = ['get', 'put']

    @action(detail=True, methods=('put',), permission_classes=(IsAuthenticated,))
    def match(self, request, pk=None):
        if int(pk) != request.user.id:
            if receiver := CustomUser.objects.match(pk, request.user.id):
                if receiver.user_sender:
                    if receiver.user_sender[0].is_sympathy == 'OK':
                        return Response(
                            {'detail': 'Пара уже выразила взаимную мимпатию.'},
                            status=status.HTTP_200_OK,
                        )
                    Match.objects.filter(id=pk).update(is_sympathy='OK')
                    match_send_mail(request.user, receiver)
                    return Response(
                        {'detail': 'Взаимность!.'},
                        status=status.HTTP_200_OK,
                    )

                _match = Match.objects.get_or_create(
                    sender=request.user, receiver=receiver
                )
                if _match[1]:
                    return Response(
                        {
                            'detail': f'Вы выразили симпатию, {receiver.first_name} скоро вам ответит.'
                        },
                        status=status.HTTP_201_CREATED,
                    )

                _match[0].is_sympathy = 'OK'
                _match[0].save(update_fields=['is_sympathy'])
                match_send_mail(request.user, receiver)
                return Response({'detail': 'Взаимность!.'}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('get',), permission_classes=(IsAuthenticated,))
    def distance(self, request, pk=None):
        sen = request.user
        rec = get_object_or_404(CustomUser, id=self.kwargs.get('pk'))

        if all((sen.latitude, sen.longitude, rec.latitude, rec.longitude)):
            km = get_distance(sen.latitude, sen.longitude, rec.latitude, rec.longitude)
            return Response({'detail': f'{km} км от вас.'})
        return Response({'detail': 'У пользователя отключена геопозиция.'})


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter

    def get_queryset(self):
        return CustomUser.objects.cactom(self.request.user)

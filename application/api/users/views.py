from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.users.serializers import UserCreateSerializer
from core.services import match_send_mail
from users.models import CustomUser, Match


class UserCreateViewSet(GenericViewSet, CreateModelMixin):
    http_method_names = ['post']
    serializer_class = UserCreateSerializer


class MatchViewSet(RetrieveModelMixin, GenericViewSet):
    http_method_names = ['put']

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
                    match_send_mail(request.user, receiver[0])
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

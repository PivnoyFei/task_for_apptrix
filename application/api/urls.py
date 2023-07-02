from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.users.views import MatchViewSet, UserCreateViewSet

app_name = 'api'

clients = DefaultRouter()
clients.register('create', UserCreateViewSet, 'create')
clients.register('', MatchViewSet, 'match')

urlpatterns = [
    path('clients/', include(clients.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]

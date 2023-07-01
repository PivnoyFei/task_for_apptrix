from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.users.views import UserCreateViewSet

app_name = 'api'

clients = DefaultRouter()
clients.register('create', UserCreateViewSet, basename='create')

urlpatterns = [
    path('clients/', include(clients.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]

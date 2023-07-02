from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

admin.site.site_title = 'Сайт знакомств'
admin.site.site_header = 'Сайт знакомств'
admin.site.index_title = 'Администрирование'

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)

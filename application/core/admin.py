from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.site_title = 'Сайт знакомств'
admin.site.site_header = 'Сайт знакомств'
admin.site.index_title = 'Администрирование'

admin.site.unregister(Group)

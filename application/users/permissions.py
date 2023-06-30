from django import forms
from django.core.exceptions import ValidationError

from users import ACCESS_RIGHTS


class StaffMixin:
    """Дает доступ для редактора и администратор"""
    def check_perm(self, user):
        return user.is_active and (user.is_staff or user.is_superuser)


class UpdateAndReadOnlyAdminMixin:
    """Дает доступ на просмотр и редактирование обьектов."""
    def has_change_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_module_permission(self, request):
        return self.check_perm(request.user)


class StaffRequiredUserAdminMixin(StaffMixin, UpdateAndReadOnlyAdminMixin):
    """Накладывает ограничение на редактирование собственного профиля,
    скрывает других пользователей, для всех кроме администратор."""
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(id=request.user.id)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        is_superuser = request.user.is_superuser

        if not is_superuser and obj is not None and obj == request.user:
            fieldsets = list(fieldsets)
            for index, field in enumerate(fieldsets):
                if ACCESS_RIGHTS in field:
                    fieldsets.pop(index)
            return tuple(fieldsets)
        return fieldsets

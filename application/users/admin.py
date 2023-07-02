from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from core.services import image_thumb
from users import ACCESS_RIGHTS
from users.models import Match
from users.permissions import StaffRequiredUserAdminMixin

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text=(
            '<ul>'
            '<li>Пароль не должен быть слишком похож на другую вашу личную информацию.</li>'
            '<li>Ваш пароль должен содержать как минимум 8 символов.</li>'
            '<li>Пароль не должен быть слишком простым и распространенным.</li>'
            '<li>Пароль не может состоять только из цифр.</li>'
            '</ul>'
        ),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.',
    )

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=(
            'У вас нет возможности посмотреть захешированный пароль, '
            'но вы можете изменить его, используя '
            '<a href=\"../password/\">эту форму</a>.'
        ),
    )

    class Meta:
        model = User
        fields = ('email',)

    def clean_password(self):
        return self.initial['password']


@admin.register(User)
class UserAdmin(StaffRequiredUserAdminMixin, BaseUserAdmin):
    form = UserAdminForm
    add_form = UserCreationForm
    list_display = (
        'get_full_name',
        'email',
        'is_active',
    )
    list_filter = ('is_staff', 'is_superuser')
    readonly_fields = ('get_full_name',)
    fieldsets = (
        (
            'персональная информация',
            {
                'fields': (
                    ('last_name', 'first_name'),
                    ('email', 'gender'),
                    ('_image', 'get_thumb'),
                    'password',
                )
            },
        ),
        (
            ACCESS_RIGHTS,
            {
                'fields': (
                    ('is_staff', 'is_superuser'),
                    'is_active',
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'fields': (
                    ('last_name', 'first_name'),
                    ('email', 'gender'),
                    ('_image', 'get_thumb'),
                    ('is_staff', 'is_superuser'),
                    'is_active',
                    ('password1', 'password2'),
                ),
            },
        ),
    )
    search_fields = (
        'first_name',
        'last_name',
    )
    ordering = ('first_name',)
    readonly_fields = ('get_thumb',)

    @admin.display(description='Фамилия Имя')
    def get_full_name(self, obj):
        return f'{obj.last_name} {obj.first_name}'

    @admin.display(description='миниатюра')
    def get_thumb(self, obj):
        return image_thumb(obj._image)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'sender',
        'receiver',
        'is_sympathy',
    )
    readonly_fields = (
        'sender',
        'receiver',
        'is_sympathy',
    )

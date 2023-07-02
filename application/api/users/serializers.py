from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

from api.core.fields import CroppedImage
from users.models import CustomUser


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'gender',
            'email',
            'password',
            '_image',
        )


class UserSerializer(DjoserUserSerializer):
    image = CroppedImage(img_size='320x320', source='_image')
    gender = serializers.SerializerMethodField()
    distance = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'gender',
            'email',
            'image',
            'distance',
        )

    def get_gender(self, obj):
        return obj.get_gender_display()

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data['distance'] = round(instance.distance, 1) if instance.distance else 0
        return data

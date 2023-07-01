from rest_framework import serializers
from sorl.thumbnail import get_thumbnail


class WEBPImage(serializers.Field):
    @staticmethod
    def convert_image(image, size):
        return get_thumbnail(
            image,
            size,
            quality=75,
            crop='center',
            format='WEBP',
        )

    def build_absolute_uri(self, path):
        return self.context.get('request').build_absolute_uri(path)

    def to_representation(self, value):
        if value:
            size = f'{value.width}x{value.height}'
            return self.build_absolute_uri(self.convert_image(value, size).url)


class CroppedImage(WEBPImage):
    def __init__(self, img_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img_size = img_size

    def to_representation(self, value):
        if value:
            return self.build_absolute_uri(self.convert_image(value, self.img_size).url)
        return None

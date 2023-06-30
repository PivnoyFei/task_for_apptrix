from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from PIL import Image

from config.settings import IMAGE_UPLOAD_MAX_SIZE


class WEBPFieldFile(ImageFieldFile):
    def save(self, name, content, save=True):
        """Сохраняет загруженные фото в формате WEBP
        уменьшает размер изображения с сохранением пропорций."""
        content.file.seek(0)
        filename, extension = name.rsplit('.', 1)
        if '/' not in name or extension.upper() != 'WEBP':
            image = Image.open(content.file).convert('RGB')

            width, height = image.size
            if width > IMAGE_UPLOAD_MAX_SIZE[0]:
                new_height = int(IMAGE_UPLOAD_MAX_SIZE[0] * height / width)
                new_width = int(new_height * width / height)
                image = image.resize((new_width, new_height), Image.ANTIALIAS)
                width, height = new_width, new_height

            if height > IMAGE_UPLOAD_MAX_SIZE[1]:
                new_width = int(IMAGE_UPLOAD_MAX_SIZE[1] * width / height)
                new_height = int(new_width * height / width)
                image = image.resize((new_width, new_height), Image.ANTIALIAS)

            image_bytes = BytesIO()
            image.save(image_bytes, format="WEBP", quality=85)
            image_content_file = ContentFile(image_bytes.getvalue(), f'{filename}.webp')
            super().save(f'{filename}.webp', image_content_file, save)


class WEBPField(models.ImageField):
    attr_class = WEBPFieldFile

from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from PIL import Image

from config.settings import IMAGE_UPLOAD_MAX_SIZE
from core.services import image_upload_max_size


class WEBPFieldFile(ImageFieldFile):
    """Класс наследник от ImageFieldFile, который производит
    сохранение файла с автоматической конвертацией в WEBP формат."""

    def save(self, name, content, save=True):
        """Переопределён метод save().
        Сохраняет загруженные фото в формате WEBP
        уменьшает размер изображения с сохранением пропорций."""
        content.file.seek(0)
        filename, extension = name.rsplit('.', 1)
        if '/' not in name or extension.upper() != 'WEBP':
            image = Image.open(content.file).convert('RGB')
            image = image_upload_max_size(image, IMAGE_UPLOAD_MAX_SIZE)
            image_bytes = BytesIO()
            image.save(image_bytes, format="WEBP", quality=85)
            image_content_file = ContentFile(image_bytes.getvalue(), f'{filename}.webp')
            super().save(f'{filename}.webp', image_content_file, save)


class WEBPField(models.ImageField):
    """Класс наследник от ImageField, который использует WEBPFieldFile вместо ImageFieldFile."""

    attr_class = WEBPFieldFile

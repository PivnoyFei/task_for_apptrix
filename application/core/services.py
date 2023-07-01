from django.utils.safestring import mark_safe
from PIL import Image, ImageFilter

from config.settings import WATERMARK_PATH


def image_thumb(image):
    if image:
        return mark_safe(f'<img height="160" src="{image.url}">')
    return 'Нет изображения'


def image_upload_max_size(image, max_size):
    """Используеться в WEBPFieldFile.
    Не уверен что достаточно надежно выносить эту функцию сюда."""
    width, height = image.size
    if width > max_size[0]:
        new_height = int(max_size[0] * height / width)
        new_width = int(new_height * width / height)
        image = image.resize((new_width, new_height), Image.ANTIALIAS)
        width, height = new_width, new_height

    if height > max_size[1]:
        new_width = int(max_size[1] * width / height)
        new_height = int(new_width * height / width)
        image = image.resize((new_width, new_height), Image.ANTIALIAS)

    return image


def image_watermark(image):
    """Накладывает водяной знак на аватарку."""
    image = Image.open(image)
    width, height = image.size
    watermark = Image.open(WATERMARK_PATH).convert("L")
    watermark = watermark.point(lambda x: 255 if x > 50 else 0)
    watermark = image_upload_max_size(watermark, (width // 2, height // 2))
    watermark = watermark.filter(ImageFilter.CONTOUR)
    watermark = watermark.point(lambda x: 0 if x == 255 else 255)
    watermark.putalpha(50)
    image.paste(watermark, (width // 4, height // 4), watermark)
    return image

from django.utils.safestring import mark_safe


def image_thumb(image):
    if image:
        return mark_safe(f'<img height="160" src="{image.url}">')
    return 'Нет изображения'

from django.db import models
from sorl.thumbnail import get_thumbnail


class ThumbnailMixin:
    def _get_thumbnail(self, size, image=None):
        if image:
            return get_thumbnail(
                image,
                size,
                quality=75,
                crop='center',
                format='WEBP',
            )
        return ''

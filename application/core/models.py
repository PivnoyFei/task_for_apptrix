from django.db import models
from sorl.thumbnail import get_thumbnail


class Timestamps(models.Model):
    created_at = models.DateTimeField(
        'созданно',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        'изменено',
        auto_now=True,
    )

    class Meta:
        abstract = True


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

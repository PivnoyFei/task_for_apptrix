import os

from django.core.exceptions import ValidationError

ALLOWED_UPLOAD_IMAGES = ('.jpg', '.jpeg', '.png', '.webp')


def validate_image(image):
    extension = os.path.splitext(image.name)[1].lower()
    if extension not in ALLOWED_UPLOAD_IMAGES:
        raise ValidationError(
            f"Допускаются только следующие форматы изобращения {ALLOWED_UPLOAD_IMAGES}"
        )
    if image.size > 5_242_880:
        raise ValidationError(f"Максимальный размер файла 5MB")

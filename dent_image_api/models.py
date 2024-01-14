import os

from django.core.exceptions import ValidationError
from django.db import models

from dent_image import settings


class Image(models.Model):
    file = models.ImageField(upload_to="images/")
    name = models.CharField(max_length=200, blank=False)

    def delete(self, *args, **kwargs):
        if self.file:
            file_path = os.path.join(settings.MEDIA_ROOT, self.file.name)
            if os.path.exists(file_path):
                os.remove(file_path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Annotation(models.Model):
    image = models.ForeignKey(
        Image, related_name="annotations", on_delete=models.CASCADE
    )
    class_id = models.CharField(max_length=100)
    shape = models.JSONField()
    tags = models.JSONField()
    meta = models.JSONField()

    relations = models.JSONField(null=True, blank=True)
    surface = models.JSONField(null=True, blank=True)

    def clean(self):
        # Validate shape
        required_shape_keys = ["start_x", "start_y", "end_x", "end_y"]
        if self.shape and not all(k in self.shape for k in required_shape_keys):
            raise ValidationError(
                "Shape must include start_x, start_y, end_x, and end_y."
            )
        if self.shape and not all(
            isinstance(self.shape[k], int)
            for k in self.shape
            if k in required_shape_keys
        ):
            raise ValidationError("Shape coordinates must be integers.")

        # Validate tags
        if self.tags and not isinstance(self.tags, list):
            raise ValidationError("Tags must be a list.")
        if self.tags and not all(isinstance(tag, (str, int)) for tag in self.tags):
            raise ValidationError("Tags must be a list of strings or integers.")

        # Validate meta
        if self.meta:
            if "confirmed" in self.meta and not isinstance(
                self.meta["confirmed"], bool
            ):
                raise ValidationError("Meta 'confirmed' must be a boolean.")
            if "confidence_percent" in self.meta and not isinstance(
                self.meta["confidence_percent"], (float, int)
            ):
                raise ValidationError(
                    "Meta 'confidence_percent' must be a float or integer."
                )
            if "confidence_percent" in self.meta and not (
                0 <= self.meta["confidence_percent"] <= 1
            ):
                raise ValidationError("'confidence_percent' must be between 0 and 1.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def is_confirmed(self):
        return self.meta.get("confirmed", False)

    def __str__(self):
        return f"Annotation {self.id} for {self.image.name}"

from django.core.exceptions import ValidationError
from django.db import models


class Image(models.Model):
    file = models.ImageField(upload_to="images/")
    name = models.CharField(max_length=200, blank=False)

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

    def clean(self):
        if not all(k in self.shape for k in ("start_x", "start_y", "end_x", "end_y")):
            raise ValidationError(
                "Shape must include start_x, start_y, end_x, and end_y."
            )
        if not all(
            isinstance(self.shape[k], int)
            for k in ("start_x", "start_y", "end_x", "end_y")
        ):
            raise ValidationError("Shape coordinates must be integers.")

        if not isinstance(self.tags, list) or not all(
            isinstance(tag, (str, int)) for tag in self.tags
        ):
            raise ValidationError("Tags must be a list of strings or integers.")

        if "confirmed" not in self.meta or not isinstance(self.meta["confirmed"], bool):
            raise ValidationError("Meta must include a boolean 'confirmed'.")
        if "confidence_percent" not in self.meta or not isinstance(
            self.meta["confidence_percent"], (float, int)
        ):
            raise ValidationError(
                "Meta must include a 'confidence_percent' as a float."
            )
        if not (0 <= self.meta["confidence_percent"] <= 1):
            raise ValidationError("'confidence_percent' must be between 0 and 1.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def is_confirmed(self):
        return self.meta.get("confirmed", False)

    def __str__(self):
        return f"Annotation {self.id} for {self.image.name}"

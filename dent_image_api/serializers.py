import json
import os

from django.db import transaction
from rest_framework import serializers
from rest_framework.fields import empty

from .models import Annotation, Image


class StrictFieldsMixin:
    def to_internal_value(self, data):
        allowed_fields = set(self.fields)
        allowed_fields.add("csrfmiddlewaretoken")
        extra_fields = set(data) - allowed_fields
        if extra_fields:
            raise serializers.ValidationError(
                {"non_field_errors": [f"Unexpected fields provided: {extra_fields}"]}
            )

        return super().to_internal_value(data)


class NonHTMLListSerializer(serializers.ListSerializer):
    def get_value(self, dictionary):
        """
        Given the input dictionary, return the field value.
        """
        # We override the default get_value method of ListSerializer to remove support
        # lists in HTML forms.
        return dictionary.get(self.field_name, empty)


class AnnotationSerializer(StrictFieldsMixin, serializers.ModelSerializer):
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    shape = serializers.JSONField()
    tags = serializers.ListField(child=serializers.CharField())
    meta = serializers.JSONField()
    relations = serializers.JSONField(required=False)
    surface = serializers.JSONField(required=False)

    class Meta:
        model = Annotation
        fields = [
            "id",
            "image",
            "class_id",
            "shape",
            "tags",
            "meta",
            "relations",
            "surface",
        ]


class AnnotationsInImageSerializer(AnnotationSerializer):
    image = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(), required=False
    )


class ImageSerializer(StrictFieldsMixin, serializers.ModelSerializer):
    annotations = NonHTMLListSerializer(
        child=AnnotationsInImageSerializer(), required=False
    )

    class Meta:
        model = Image
        fields = ["id", "file", "name", "annotations"]

    def to_internal_value(self, data):
        if "annotations" in data and isinstance(data["annotations"], str):
            try:
                data["annotations"] = json.loads(data["annotations"])
            except json.JSONDecodeError:
                raise serializers.ValidationError(
                    {"annotations": ["Invalid JSON format for annotations"]}
                )
        return super().to_internal_value(data)

    def validate(self, attrs):
        if "annotations" in attrs:
            if not isinstance(attrs["annotations"], list):
                raise serializers.ValidationError(
                    {"annotations": ["Annotations must be a list."]}
                )

        return super().validate(attrs)

    def create(self, validated_data):
        with transaction.atomic():
            annotations_data = validated_data.pop("annotations", [])
            image = Image.objects.create(**validated_data)

            for annotation_data in annotations_data:
                Annotation.objects.create(image=image, **annotation_data)

        return image

    def update(self, instance, validated_data):
        old_file_path = None

        if "name" in validated_data:
            instance.name = validated_data.get("name", instance.name)

        if "file" in validated_data:
            old_file_path = instance.file.path
            instance.file = validated_data.get("file")

        instance.save()

        # after save we will got a new copy of file, so we can remove old one
        new_file_path = instance.file.path if instance.file else None
        if (
            old_file_path
            and old_file_path != new_file_path
            and os.path.isfile(old_file_path)
        ):
            os.remove(old_file_path)

        if "annotations" in validated_data:
            annotations_data = validated_data.pop("annotations")
            existing_annotations = {
                anno.id: anno for anno in instance.annotations.all()
            }

            for annotation_data in annotations_data:
                annotation_id = annotation_data.get("id")
                if annotation_id and annotation_id in existing_annotations:
                    anno_instance = existing_annotations[annotation_id]
                    for key, value in annotation_data.items():
                        setattr(anno_instance, key, value)
                    anno_instance.save()
                elif not annotation_id:
                    Annotation.objects.create(image=instance, **annotation_data)

            incoming_ids = set(
                anno_data.get("id")
                for anno_data in annotations_data
                if "id" in anno_data
            )
            for anno_id, anno_instance in existing_annotations.items():
                if anno_id not in incoming_ids:
                    anno_instance.delete()

        return instance

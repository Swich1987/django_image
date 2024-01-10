import pytest
from django.core.exceptions import ValidationError
from .models import Image, Annotation


@pytest.fixture
def image():
    return Image.objects.create(name="Test Image", file="path/to/test/image.jpg")


@pytest.fixture
def annotation(image):
    return Annotation.objects.create(
        image=image,
        class_id="tooth",
        shape={"start_x": 100, "start_y": 100, "end_x": 200, "end_y": 200},
        tags=["48"],
        meta={"confirmed": True, "confidence_percent": 0.99},
    )


def test_create_valid_image(db):
    image = Image.objects.create(name="Valid Image", file="path/to/valid/image.jpg")
    assert image.name == "Valid Image"


def test_create_valid_annotation(db, image):
    annotation = Annotation.objects.create(
        image=image,
        class_id="caries",
        shape={"start_x": 10, "start_y": 20, "end_x": 30, "end_y": 40},
        tags=["49"],
        meta={"confirmed": False, "confidence_percent": 0.87},
    )
    assert annotation.class_id == "caries"


def test_annotation_shape_validation(db, image):
    with pytest.raises(ValidationError):
        Annotation.objects.create(
            image=image,
            class_id="caries",
            shape={
                "start_x": "not an integer",
                "start_y": 20,
                "end_x": 30,
                "end_y": 40,
            },
            tags=["49"],
            meta={"confirmed": False, "confidence_percent": 0.87},
        )


def test_annotation_meta_validation(db, image):
    with pytest.raises(ValidationError):
        Annotation.objects.create(
            image=image,
            class_id="caries",
            shape={"start_x": 10, "start_y": 20, "end_x": 30, "end_y": 40},
            tags=["49"],
            meta={"confirmed": "not a boolean", "confidence_percent": 0.87},
        )


def test_annotation_confidence_percent_validation(db, image):
    with pytest.raises(ValidationError):
        Annotation.objects.create(
            image=image,
            class_id="caries",
            shape={"start_x": 10, "start_y": 20, "end_x": 30, "end_y": 40},
            tags=["49"],
            meta={
                "confirmed": True,
                "confidence_percent": 1.5,  # Invalid confidence_percent
            },
        )

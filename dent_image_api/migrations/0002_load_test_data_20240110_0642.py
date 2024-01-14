# Generated by Django 5.0 on 2024-01-10 06:42
from django.core.files import File
from django.db import migrations


def add_test_data(apps, schema_editor):
    ImageModel = apps.get_model("dent_image_api", "Image")
    AnnotationModel = apps.get_model("dent_image_api", "Annotation")

    with open("/app/tests/media/images/dental-x-ray.jpeg", "rb") as file1:
        image1 = ImageModel(name="Dental X-Ray")
        image1.file.save("dental-x-ray.jpeg", File(file1), save=True)

    with open("/app/tests/media/images/dental-x-ray_2.jpeg", "rb") as file2:
        image2 = ImageModel(name="Dental X-Ray 2")
        image2.file.save("dental-x-ray_2.jpeg", File(file2), save=True)

    annotations1 = [
        {
            "class_id": "tooth",
            "shape": {"start_x": 100, "start_y": 100, "end_x": 200, "end_y": 200},
            "tags": ["48"],
            "meta": {"confirmed": True, "confidence_percent": 0.99},
        }
    ]

    for annotation_data in annotations1:
        annotation = AnnotationModel(image=image1, **annotation_data)
        annotation.save()


def remove_test_data(apps, schema_editor):
    ImageModel = apps.get_model("dent_image_api", "Image")
    ImageModel.objects.filter(name__in=["Dental X-Ray", "Dental X-Ray 2"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("dent_image_api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_test_data, reverse_code=remove_test_data),
    ]

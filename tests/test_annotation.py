import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dent_image_api.models import Annotation, Image
from tests import constants


class AnnotationTests(APITestCase):
    def setUp(self):
        self.image_file = SimpleUploadedFile(
            name="test_image.jpg",
            content=open(constants.TEST_IMAGE_PATH, "rb").read(),
            content_type="image/jpeg",
        )
        self.image = Image.objects.create(name="Test Image", file=self.image_file)

        self.annotation = Annotation.objects.create(
            image=self.image,
            class_id="tooth",
            shape={"start_x": 100, "start_y": 100, "end_x": 200, "end_y": 200},
            tags=["48"],
            meta={"confirmed": True, "confidence_percent": 0.99},
        )

        self.single_annotation_url = reverse(
            "image-annotation-detail",
            kwargs={"image_id": self.image.pk, "pk": self.annotation.pk},
        )

        self.all_annotations_url = reverse(
            "image-annotations", kwargs={"image_id": self.image.pk}
        )

    def tearDown(self):
        self.image.delete()
        self.annotation.delete()

    def test_create_annotation(self):
        data = {
            "image": self.image.pk,
            "class_id": "caries",
            "shape": {"start_x": 50, "start_y": 50, "end_x": 150, "end_y": 150},
            "tags": ["49"],
            "meta": {"confirmed": False, "confidence_percent": 0.85},
        }
        response = self.client.post(self.all_annotations_url, data, format="json")
        self.assertEqual(
            status.HTTP_201_CREATED,
            response.status_code,
            f"Expected HTTP 201 Created, got HTTP {response.status_code}. Response data: {response.data}",
        )

    def test_get_single_annotation(self):
        response = self.client.get(self.single_annotation_url)
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
            f"Expected HTTP 200 OK, got HTTP {response.status_code}. Response data: {response.data}",
        )
        self.assertEqual(self.annotation.id, response.data["id"])

    def test_get_all_annotations_for_image(self):
        response = self.client.get(self.all_annotations_url)
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
            f"Expected HTTP 200 OK, got HTTP {response.status_code}. Response data: {response.data}",
        )
        self.assertIn(self.annotation.id, [item["id"] for item in response.data])

    def test_patch_annotation(self):
        # Only update class_id and the confidence_percent part of the meta
        patch_data = {
            "class_id": "patched_caries",
            "meta": {"confidence_percent": 0.75},
        }

        response = self.client.patch(
            self.single_annotation_url, patch_data, format="json"
        )

        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
            f"Expected HTTP 200 OK for PATCH, got HTTP {response.status_code}. Response data: {response.data}",
        )

        # Fetch the updated annotation to check if the partial update worked
        patched_annotation = Annotation.objects.get(pk=self.annotation.pk)
        self.assertEqual("patched_caries", patched_annotation.class_id)
        self.assertEqual(0.75, patched_annotation.meta["confidence_percent"])

    def test_patch_annotation_with_invalid_field(self):
        invalid_patch_data = {
            "nonexistent_field": "some_value",
        }

        response = self.client.patch(
            self.single_annotation_url, invalid_patch_data, format="json"
        )

        self.assertNotEqual(
            status.HTTP_200_OK,
            response.status_code,
            (
                f"Expected non-200 HTTP status for PATCH with invalid field, got"
                f" HTTP {response.status_code}. Response data: {response.data}"
            ),
        )

    def test_put_annotation(self):
        # Full data representation for the update, typically including all fields of the resource
        put_data = {
            "image": self.image.pk,
            "class_id": "updated_caries",
            "shape": {"start_x": 60, "start_y": 60, "end_x": 160, "end_y": 160},
            "tags": ["updated_49"],
            "meta": {"confirmed": True, "confidence_percent": 0.95},
        }

        response = self.client.put(self.single_annotation_url, put_data, format="json")

        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
            f"Expected HTTP 200 OK for PUT, got HTTP {response.status_code}. Response data: {response.data}",
        )

        # Fetch the updated annotation to check if the full update worked
        updated_annotation = Annotation.objects.get(pk=self.annotation.pk)
        self.assertEqual("updated_caries", updated_annotation.class_id)
        self.assertEqual(0.95, updated_annotation.meta["confidence_percent"])

    def test_put_annotation_with_incomplete_data(self):
        incomplete_put_data = {
            # Omitting required fields like 'class_id', 'shape', etc.
            "tags": ["updated_49"],
            "meta": {"confirmed": True, "confidence_percent": 0.95},
        }

        response = self.client.put(
            self.single_annotation_url, incomplete_put_data, format="json"
        )

        self.assertNotEqual(
            status.HTTP_200_OK,
            response.status_code,
            f"Expected non-200 HTTP status for PUT with incomplete data, got HTTP {response.status_code}. Response data: {response.data}",
        )

    def test_put_annotation_with_incorrect_data_type(self):
        incorrect_type_data = {
            "class_id": "updated_caries",
            "shape": "This should be a dictionary, not a string",
            "tags": ["updated_49"],
            "meta": {
                "confirmed": True,
                "confidence_percent": "Should be a float, not a string",
            },
        }

        response = self.client.put(
            self.single_annotation_url, incorrect_type_data, format="json"
        )

        self.assertNotEqual(
            status.HTTP_200_OK,
            response.status_code,
            f"Expected non-200 HTTP status for PUT with incorrect data type, got HTTP {response.status_code}. Response data: {response.data}",
        )

    def test_delete_annotation(self):
        response = self.client.delete(self.single_annotation_url)
        self.assertEqual(
            status.HTTP_204_NO_CONTENT,
            response.status_code,
            f"Expected HTTP 204 No Content, got HTTP {response.status_code}. Response data: {response.data}",
        )
        with self.assertRaises(Annotation.DoesNotExist):
            Annotation.objects.get(pk=self.annotation.pk)

    def test_create_annotation_with_invalid_data(self):
        invalid_data = {
            # Assume class_id is required and the rest of the necessary fields are missing
            "class_id": "caries",
        }
        response = self.client.post(
            self.all_annotations_url, invalid_data, format="json"
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST,
            response.status_code,
            f"Expected HTTP 400 Bad Request, got HTTP {response.status_code}. Response data: {response.data}",
        )

    def test_get_confirmed_annotations_external_direction(self):
        print("Image count:", Image.objects.count())  # Should be > 0
        print(
            "Annotation count for image:",
            Annotation.objects.filter(image=self.image).count(),
        )

        # Assume there's a way to mark an annotation as not confirmed
        unconfirmed_annotation = Annotation.objects.create(
            image=self.image,
            class_id="caries",
            shape={"start_x": 150, "start_y": 150, "end_x": 250, "end_y": 250},
            tags=["47"],
            meta={"confirmed": False, "confidence_percent": 0.80},
        )

        # Define a new URL or parameter to fetch annotations in the external direction
        external_direction_url = self.all_annotations_url + "?direction=external"
        print(f"{external_direction_url=}")

        response = self.client.get(external_direction_url)
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
            f"Expected HTTP 200 OK, got HTTP {response.status_code}. Response data: {response.context}",
        )
        # Iterate through annotations and check if all are confirmed
        for annotation in response.data:
            self.assertTrue(
                annotation["meta"]["confirmed"], "Unconfirmed annotation was returned."
            )

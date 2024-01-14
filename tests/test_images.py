import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dent_image_api.models import Image, Annotation
from tests import constants


class ImageTests(APITestCase):
    def setUp(self):
        self.image_file = SimpleUploadedFile(
            name="test_image.jpg",
            content=open(constants.TEST_IMAGE_PATH, "rb").read(),
            content_type="image/jpeg",
        )
        self.image_file_2 = SimpleUploadedFile(
            name="test_image_2.jpg",
            content=open(constants.TEST_IMAGE_2_PATH, "rb").read(),
            content_type="image/jpeg",
        )

        self.image = Image.objects.create(name="Test Image", file=self.image_file)
        self.image_2 = Image.objects.create(name="Test Image 2", file=self.image_file_2)

        self.list_url = reverse("image-list")
        self.detail_url = reverse("image-detail", kwargs={"pk": self.image.pk})

    def tearDown(self):
        all_images = Image.objects.all()
        for image in all_images:
            image.delete()

    def test_create_image_without_annotation(self):
        with open(constants.TEST_IMAGE_PATH, "rb") as image_file:
            response = self.client.post(
                self.list_url, {"name": "New Image", "file": image_file}
            )
        self.assertEqual(
            status.HTTP_201_CREATED,
            response.status_code,
            msg=f"Failed to create image without annotation. Response data: {response.data}",
        )
        created_image = Image.objects.get(name="New Image")
        if created_image:
            created_image.delete()

    def test_create_image_with_annotations(self):
        with open(constants.TEST_IMAGE_PATH, "rb") as image_file:
            # Convert the annotations list into a JSON string
            annotations_json = json.dumps(
                [
                    {
                        "class_id": "tooth",
                        "shape": {
                            "start_x": 100,
                            "start_y": 100,
                            "end_x": 200,
                            "end_y": 200,
                        },
                        "tags": ["48"],
                        "meta": {"confirmed": True, "confidence_percent": 0.99},
                    }
                ]
            )

            # Construct the multipart form data payload
            data = {
                "name": "Image with Annotations",
                "file": image_file,
                "annotations": annotations_json,  # Pass annotations as a JSON string
            }

            response = self.client.post(self.list_url, data, format="multipart")
            self.assertEqual(
                status.HTTP_201_CREATED,
                response.status_code,
                msg=f"Failed to create image with annotations. Response data: {response.data}",
            )

            self.assertTrue(
                Image.objects.filter(name="Image with Annotations").exists(),
                msg="Image with Annotations does not exist after creation.",
            )

            image = Image.objects.get(name="Image with Annotations")
            self.assertTrue(
                Annotation.objects.filter(image=image).exists(),
                msg="Annotations for the image do not exist after creation.",
            )
            image.delete()

    def test_create_image_with_invalid_data(self):
        response = self.client.post(self.list_url, {"name": "", "file": ""})
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST,
            response.status_code,
            msg=f"Invalid data unexpectedly created image. Response data: {response.data}",
        )
        image = Image.objects.filter(name="")
        if image:
            image.delete()

    def test_create_image_with_invalid_file_type(self):
        with open(constants.TEST_INVALID_IMAGE_PATH, "rb") as invalid_file:
            response = self.client.post(
                self.list_url, {"name": "Invalid File Image", "file": invalid_file}
            )
        self.assertNotEqual(
            status.HTTP_201_CREATED,
            response.status_code,
            msg=f"Invalid file type unexpectedly created image. Response data: {response.data}",
        )
        image = Image.objects.filter(name="Invalid File Image")
        assert not image

    def test_get_image_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
            msg=f"Failed to get image list. Response data: {response.data}",
        )
        self.assertEqual(
            4,  # 2 images from migrations and 2 from tests
            len(response.data),
            msg="Image list does not contain expected number of entries.",
        )

    def test_get_image_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
            msg=f"Failed to get image detail. Response data: {response.data}",
        )
        self.assertEqual(
            self.image.name,
            response.data["name"],
            msg="Image details do not match expected values.",
        )

    def test_put_image(self):
        with open(constants.TEST_IMAGE_2_PATH, "rb") as image_file:
            response = self.client.put(
                self.detail_url, {"name": "Updated with put Image", "file": image_file}
            )
            self.assertEqual(
                status.HTTP_200_OK,
                response.status_code,
                msg=f"Failed to update image. Response data: {response.data}",
            )
            self.image.refresh_from_db()
            updated_image = Image.objects.get(pk=self.image.pk)
            self.assertEqual(
                "Updated with put Image",
                updated_image.name,
                msg="Image name not updated as expected.",
            )
            self.assertEqual(
                updated_image.file.path,
                self.image.file.path,
                msg="Image file not updated as expected.",
            )

    def test_put_image_with_incomplete_data(self):
        put_data = {"name": "Incomplete Data Image"}
        response = self.client.put(self.detail_url, put_data, format="json")
        self.assertNotEqual(
            status.HTTP_200_OK,
            response.status_code,
            msg=f"Incomplete data unexpectedly updated image. Response data: {response.data}",
        )
        self.assertNotEqual(
            "Incomplete Data Image",
            Image.objects.get(pk=self.image.pk).name,
            msg="Image name updated with incomplete data.",
        )

    def test_put_image_with_incorrect_data_type(self):
        put_data = {
            "name": "Incorrect Type Image",
            "file": "This should be a file, not a string",
        }
        response = self.client.put(self.detail_url, put_data, format="json")
        self.assertNotEqual(
            status.HTTP_200_OK,
            response.status_code,
            msg=f"Incorrect data type unexpectedly updated image. Response data: {response.data}",
        )

    def test_patch_image_name(self):
        patch_data = {"name": "Patched Image Name"}
        response = self.client.patch(self.detail_url, patch_data, format="json")
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
            msg=f"Failed to patch image. Response data: {response.data}",
        )
        patched_image = Image.objects.get(pk=self.image.pk)
        self.assertEqual(
            "Patched Image Name",
            patched_image.name,
            msg="Image name not patched as expected.",
        )

    def test_patch_image_file(self):
        with open(constants.TEST_IMAGE_2_PATH, "rb") as image_file_2:
            patch_data = {"file": image_file_2}
            response = self.client.patch(
                self.detail_url, patch_data, format="multipart"
            )
            self.assertEqual(
                status.HTTP_200_OK,
                response.status_code,
                msg=f"Failed to patch image. Response data: {response.data}",
            )
            patched_image = Image.objects.get(pk=self.image.pk)
            self.assertNotEqual(
                patched_image.file.path,
                self.image.file.path,
                msg="Image file not patched as expected.",
            )
            assert constants.TEST_IMAGE_2_FILENAME in patched_image.file.path

    def test_delete_image(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(
            status.HTTP_204_NO_CONTENT,
            response.status_code,
            msg=f"Failed to delete image. Response data: {response.data}",
        )
        with self.assertRaises(
            Image.DoesNotExist, msg="Image still exists after deletion."
        ):
            Image.objects.get(pk=self.image.pk)

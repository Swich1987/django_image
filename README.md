# README

To run the project, you need to have docker and docker-compose installed.
After that, you can run the following commands:

```bash
docker-compose up
```

You can check if the project is running by accessing the root url <http://0.0.0.0:8080>

# Browsable API

After run, you can test the API through browsable API at <http://0.0.0.0:8080/api/v1/>

## Images
Browsable API link for images: <http://0.0.0.0:8080/api/v1/images/>
Browsable API link for image with id=1: <http://0.0.0.0:8080/api/v1/images/1/>

- GET /api/v1/images
  return list of all images
- POST /api/v1/images
  create a new image (with or without annotations)
- GET /api/v1/images/{id_image}
  return a single image (with or without annotations)
- PUT /api/v1/images/{id_image}
  update a single image
- DELETE /api/v1/images/{id_image}
  delete a single image

## Annotations
Browsable API link for annotations of image with id=1: <http://0.0.0.0:8080/api/v1/images/1/annotations/>
Browsable API link for annotation with id=1 of image with id=1: <http://0.0.0.0:8080/api/v1/images/1/annotations/1/>

- GET /api/v1/images/{id_image}/annotations?direction=[external|internal]
  return all annotations for an image;
  defaults to external (only confirmed findings) unless direction='internal' is specified.
- POST /api/v1/images/{id_image}/annotations
  create a new annotation of an image
- GET /api/v1/images/{id_image}/annotations/{id_annotation}
  return a single annotation of an image
- PUT /api/v1/images/{id_image}/annotations
  update annotation of an image (all at once)
- PUT /api/v1/images/{id_image}/annotations/{id_annotation}
  update annotation of an image (one at a time)
- DELETE /api/v1/images/{id_image}/annotations
  delete all annotations of an image
- DELETE /api/v1/images/{id_image}/annotations/{id_annotation}
  delete a single annotation of an image


# Manual API Testing with Curl Commands

Before running the curl commands to test the Image API, initialize the necessary environment variables. Replace the placeholder paths, URLs, and image ID with the actual values for your setup.

### Initialization
Set the environment variables:

```bash
export API_URL_IMAGES="http://0.0.0.0:8080/api/v1/images"
export TEST_IMAGE_PATH="tests/media/images/dental-x-ray.jpeg"
export TEST_IMAGE_2_PATH="tests/media/images/dental-x-ray_2.jpeg"
export TEST_INVALID_IMAGE_PATH="tests/media/images/invalid_file.txt"
export IMAGE_ID="1"  
```

Now, use the following `curl` commands to manually test the API:

### 1. Test Create Image without Annotation
```bash
curl -X POST -F "name=New Image" -F "file=@${TEST_IMAGE_PATH}" ${API_URL_IMAGES}/
```

### 2. Test Create Image with Annotations
```bash
curl -X POST \
     -H "Content-Type: multipart/form-data" \
     -F "name=Image with Annotations" \
     -F "file=@${TEST_IMAGE_PATH}" \
     -F "annotations=[{\"class_id\": \"tooth\", \"shape\": {\"start_x\": 100, \"start_y\": 100, \"end_x\": 200, \"end_y\": 200}, \"tags\": [\"48\"], \"meta\": {\"confirmed\": true, \"confidence_percent\": 0.99}}]" \
     ${API_URL_IMAGES}/
```

### 3. Test Create Image with Invalid Data
```bash
curl -X POST -F "name=" -F "file=" ${API_URL_IMAGES}/
```

### 4. Test Create Image with Invalid File Type
```bash
curl -X POST -F "name=Invalid File Image" -F "file=@${TEST_INVALID_IMAGE_PATH}" ${API_URL_IMAGES}/
```

### 5. Test Get Image List
```bash
curl -X GET ${API_URL_IMAGES}/
```

### 6. Test Get Image Detail
```bash
curl -X GET ${API_URL_IMAGES}/${IMAGE_ID}/
```

### 7. Test Put Image
```bash
curl -X PUT -F "name=Updated with put Image" -F "file=@${TEST_IMAGE_2_PATH}" ${API_URL_IMAGES}/${IMAGE_ID}/
```

### 8. Test Put Image with Incomplete Data
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Incomplete Data Image"}' ${API_URL_IMAGES}/${IMAGE_ID}/
```

### 9. Test Patch Image Name
```bash
curl -X PATCH -H "Content-Type: application/json" -d '{"name": "Patched Image Name"}' ${API_URL_IMAGES}/${IMAGE_ID}/
```

### 10. Test Patch Image File
```bash
curl -X PATCH -F "file=@${TEST_IMAGE_2_PATH}" ${API_URL_IMAGES}/${IMAGE_ID}/
```

### 11. Test Delete Image
```bash
curl -X DELETE ${API_URL_IMAGES}/${IMAGE_ID}/
```

Ensure all environment variables are correctly set and point to valid data before executing these commands. Adjust the API endpoint as needed for your specific setup.

Let's first describe all possible API endpoints:
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

- GET /api/v1/images/{id_image}/annotations
  return all annotations for an image
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

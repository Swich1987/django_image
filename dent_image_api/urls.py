from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AnnotationViewSet, ImageViewSet

router = DefaultRouter()
router.register(r"images", ImageViewSet)

annotations_list = AnnotationViewSet.as_view({"get": "list", "post": "create"})
annotation_detail = AnnotationViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "images/<int:image_id>/annotations/", annotations_list, name="image-annotations"
    ),
    path(
        "images/<int:image_id>/annotations/<int:pk>/",
        annotation_detail,
        name="image-annotation-detail",
    ),
]

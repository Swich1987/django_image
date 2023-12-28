from django.urls import path

from .views import AnnotationDetail, AnnotationList, ImageDetail, ImageList

urlpatterns = [
    path("images/", ImageList.as_view(), name="image-list"),
    path("images/<int:pk>/", ImageDetail.as_view(), name="image-detail"),
    path("annotations/", AnnotationList.as_view(), name="annotation-list"),
    path("annotations/<int:pk>/", AnnotationDetail.as_view(), name="annotation-detail"),
]

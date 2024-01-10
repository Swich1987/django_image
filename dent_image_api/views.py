from rest_framework import viewsets
from .models import Annotation, Image
from .serializers import AnnotationSerializer, ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        image_id = self.kwargs.get("image_id")
        if image_id is not None:
            queryset = queryset.filter(image_id=image_id)

        direction = self.request.query_params.get("direction")
        if direction == "external":
            queryset = queryset.filter(meta__confirmed=True)
        return queryset

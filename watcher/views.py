from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import farm
from .serializer import farmSerializer
from .utils import download_satellite_image
# Create your views here.

class farmViewSet(viewsets.ModelViewSet):
    queryset = farm.objects.all()
    serializer_class = farmSerializer

    @action(detail = True, methods = ["get"])
    def download_image(self, request, pk = None):
        farm_instance = self.get_object()
        download_satellite_image(farm_instance)
        return Response({"status": "image downloaded", "image_path": farm_instance.image_path})
    
    def retrieve(self, request, *args, **kwargs):
        farm_instance = self.get_object()
        download_satellite_image(farm_instance)  # Ensure the image is downloaded
        serializer = self.get_serializer(farm_instance)
        return Response(serializer.data)
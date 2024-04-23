from django.shortcuts import render
from rest_framework import viewsets

from .models import watcher_model
from .serializer import farmSerializer
# Create your views here.

class farmViewSet(viewsets.ModelViewSet):
    queryset = watcher_model.objects.all()
    serializer_class = farmSerializer
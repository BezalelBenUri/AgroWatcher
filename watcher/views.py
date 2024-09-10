from datetime import datetime, timedelta

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import ee

from .models import farm
from .serializer import farmSerializer
from .utils import download_satellite_image
from .utils import get_time_series
# Create your views here.

class farmViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing farm data and satellite imagery.

    This viewset provides CRUD operations (Create, Retrieve, Update, Delete) 
    for farm objects, as well as functionalities for downloading satellite 
    imagery and retrieving time series data for a specific farm.
    """
    queryset = farm.objects.all()
    serializer_class = farmSerializer

    @action(detail = True, methods = ["get"])
    def download_image(self, request, pk = None):
        """
        Downloads satellite imagery and vegetation indices for a specific farm.

        This action retrieves the latest Landsat 8 image with less than 1% cloud 
        cover for the area of the farm, calculates NDVI, NDMI, and NDWI indices, 
        downloads thumbnails of the satellite image and the indices, and saves the 
        image paths to the farm model.

        Args:
            request: The incoming HTTP request object.
            pk: The primary key of the farm object.

        Returns:
            A JSON response containing:
                - "status": "image downloaded" (success message).
                - "image_path": The path to the downloaded satellite image thumbnail.
                - "ndvi_path": The path to the downloaded NDVI thumbnail.
                - "ndmi_path": The path to the downloaded NDMI thumbnail.
                - "ndwi_path": The path to the downloaded NDWI thumbnail.
        """
        farm_instance = self.get_object()
        download_satellite_image(farm_instance)
        return Response({
            "status": "image downloaded", 
            "image_path": farm_instance.image_path,
            "ndvi_path": farm_instance.ndvi_path,
            "ndmi_path": farm_instance.ndmi_path,
            "ndwi_path": farm_instance.ndwi_path,

            })
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves details of a farm and ensures its satellite image is downloaded.

        This method overrides the default `retrieve` behavior to guarantee that 
        a satellite image is downloaded for the farm before returning its details. 
        It first retrieves the farm instance, downloads the satellite image using 
        `download_satellite_image`, and then serializes the farm data for response.

        Args:
            request: The incoming HTTP request object.
            *args: Additional positional arguments passed to the method.
            **kwargs: Additional keyword arguments passed to the method.

        Returns:
            A JSON response containing the serialized farm data.
        """
        farm_instance = self.get_object()
        download_satellite_image(farm_instance)  # Ensure the image is downloaded
        serializer = self.get_serializer(farm_instance)
        return Response(serializer.data)
    
    @action(detail = True, methods = ["get"])
    def time_series(self, request, pk = None):
        """
        Retrieves time series data for vegetation indices of a specific farm.

        This action calculates the mean NDVI, NDMI, and NDWI values over the 
        past year for the area of the farm. It retrieves the farm instance, 
        defines a year-long time window, converts the farm's geometry to Earth 
        Engine format, and then calls `get_time_series` to obtain the time series 
        data. Finally, it returns a JSON response containing the farm name and 
        the time series data.

        Args:
            request: The incoming HTTP request object.
            pk: The primary key of the farm object.

        Returns:
            A JSON response containing:
                - "farm": The name of the farm.
                - "time_series": A list of dictionaries containing date and 
                                corresponding mean values for NDVI, NDMI, and NDWI.
        """
        farm_instance = self.get_object()

        end_date = datetime.today()
        start_date = end_date - timedelta(days = 365)
        
        # Convert the geometry to a format suitable for GEE
        geom = farm_instance.geom.geojson
        geometry = ee.Geometry.MultiPolygon(eval(geom)["coordinates"])

        # Get the time series data
        time_series_data = get_time_series(
            geometry = geometry,
            start_date = start_date.strftime('%Y-%m-%d'),
            end_date = end_date.strftime('%Y-%m-%d')
        )

        return Response({
            "farm": farm_instance.name,
            "time_series": time_series_data
        })

import ee
import os
import json
import wget
from django.conf import settings
from .models import farm

# Authenticate and initialize the Earth Engine API
ee.Authenticate()
ee.Initialize(project="ee-bezalelbenuri")


def download_satellite_image(farm):
    try:
        # Convert the geometry to a format suitable for GEE
        geom = farm.geom.geojson
        geometry = ee.Geometry.MultiPolygon(eval(geom)["coordinates"])

        print(f"Processed Geometry: {geometry.getInfo()}")  # Debug print statement

        # Get the latest Landsat 8 image
        image = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
            .filterBounds(geometry) \
            .sort('DATE_ACQUIRED', False) \
            .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', 0)) \
            .first()
        
        # Define visualization parameters
        vis_params = {
            "bands": ["B4", "B3", "B2"],
            "min": 0,
            "max": 3000,
            "gamma": 1.4,
        }

        # Get a URL for the image
        url = image.getThumbURL({
            "min": 0,
            "max": 3000,
            "region": geometry,
            "dimensions": 512,
            "format": "png"
        })

        print(f"Image URL: {url}")  # Debug print statement

        # Define the local file path
        image_folder = os.path.join(settings.BASE_DIR, 'watcher', 'generated', 'satellite_images')
        os.makedirs(image_folder, exist_ok=True)
        image_path = os.path.join(image_folder, f"{farm.id}.png")

        # Download the image
        os.system(f'wget -O {image_path} "{url}"')

        # Save the image path to the model
        farm.image_path = os.path.join('generated/satellite_images', f'{farm.id}.png')
        farm.save()
    except Exception as e:
        print(f"Error downloading satellite image: {e}")

import ee
import os
import json
import wget
from django.conf import settings
from .models import farm

# Authenticate and initialize the Earth Engine API
ee.Authenticate()
ee.Initialize(project="ee-bezalelbenuri")


def calculate_indices(image, geometry):
    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
    ndmi = image.normalizedDifference(["B8", "B11"]).rename("NDMI")
    ndwi = image.normalizedDifference(["B3", "B11"]).rename("NDWI")

    return ndvi, ndmi, ndwi

def get_image_url(image, geometry, vis_params):
    return image.getThumbURL({
        "min": vis_params.get("min", 0),
        "max": vis_params.get("max", 3000),
        "region": geometry,
        "dimensions": 512,
        "format": "png"
    })

def download_image(url, path):
    os.makedirs(os.path.dirname(path), exist_ok = True)
    os.system(f'wget -O {path} "{url}"')


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

        # Get satellite image URL
        satellite_url = get_image_url(image, geometry, vis_params)
        print(f"Image URL: {satellite_url}")  # Debug print statement
        satellite_path = os.path.join(settings.BASE_DIR, 'watcher', 'generated', 'satellite_images', f"{farm.id}_satellite.png")
        download_image(satellite_url, satellite_path)

        # calculate indices
        ndvi, ndmi, ndwi = calculate_indices(image, geometry)

        # Get URLS for indices
        ndvi_url = get_image_url(ndvi, geometry, {"min": -1, "max": 1})
        ndmi_url = get_image_url(ndmi, geometry, {"min": -1, "max": 1})
        ndwi_url = get_image_url(ndwi, geometry, {"min": -1, "max": 1})

        # Define local file paths
        ndvi_path = os.path.join(settings.BASE_DIR, "watcher", "generated", "ndvi_images", f"{farm.id}_ndvi.png")
        ndmi_path = os.path.join(settings.BASE_DIR, "watcher", "generated", "ndmi_images", f"{farm.id}_ndmi.png")
        ndwi_path = os.path.join(settings.BASE_DIR, "watcher", "generated", "ndwi_images", f"{farm.id}_ndwi.png")

        # Download the images
        download_image(ndvi_url, ndvi_path)
        download_image(ndmi_url, ndmi_path)
        download_image(ndwi_url, ndwi_path)

        # Save the image path to the model
        farm.image_path = os.path.join('generated/satellite_images', f'{farm.id}_satellite.png')
        farm.ndvi_path = os.path.join('generated/ndvi_images', f'{farm.id}_ndvi.png')
        farm.ndmi_path = os.path.join('generated/ndmi_images', f'{farm.id}_ndmi.png')
        farm.ndwi_path = os.path.join('generated/ndmi_images', f'{farm.id}_ndmi.png')
        farm.save()
    except Exception as e:
        print(f"Error downloading satellite image: {e}")

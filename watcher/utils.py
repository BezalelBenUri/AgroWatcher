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
    """
    Calculates the Normalized Difference Vegetation Index (NDVI), 
    Normalized Difference Moisture Index (NDMI), and 
    Normalized Difference Water Index (NDWI) 
    from an Earth Engine image.

    Args:
        image: An Earth Engine image object.
        geometry: An Earth Engine geometry object representing the area of interest.

    Returns:
        A tuple containing three Earth Engine image objects: NDVI, NDMI, and NDWI.
    """
    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
    ndmi = image.normalizedDifference(["B8", "B11"]).rename("NDMI")
    ndwi = image.normalizedDifference(["B3", "B11"]).rename("NDWI")

    return ndvi, ndmi, ndwi

def get_image_url(image, geometry, vis_params):
    """
    Generates a URL for a thumbnail of an Earth Engine image.

    Args:
        image: An Earth Engine image object.
        geometry: An Earth Engine geometry object representing the area of interest.
        vis_params: A dictionary containing visualization parameters for the image.

    Returns:
        A string containing the URL for the thumbnail image.
    """
    return image.getThumbURL({
        "min": vis_params.get("min", 0),
        "max": vis_params.get("max", 3000),
        "region": geometry,
        "dimensions": 512,
        "palette": vis_params.get("palette"),
        "format": "png"
    })

def download_image(url, path):
    """
    Downloads a file from a URL to a specified path.

    Args:
        url: The URL of the file to download.
        path: The path where the downloaded file should be saved.
    """
    os.makedirs(os.path.dirname(path), exist_ok = True)
    os.system(f'wget -O {path} "{url}"')


def download_satellite_image(farm):
    """
    Downloads a satellite image and vegetation indices for a given farm.

    This function retrieves the latest Landsat 8 image with less than 1% cloud 
    cover for the area of the farm, calculates NDVI, NDMI, and NDWI indices, 
    downloads thumbnails of the satellite image and the indices, and saves the 
    image paths to the farm model.

    Args:
        farm: A farm object from the .models module.
    """
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

        # Define visualization parameters for indices
        ndvi_vis_params = {"min": -1, "max": 1, "palette": ["blue", "white", "green"]}
        ndmi_vis_params = {"min": -1, "max": 1, "palette": ["white", "blue"]}
        ndwi_vis_params = {"min": -1, "max": 1, "palette": ["white", "cyan"]}


        # Get URLS for indices
        ndvi_url = get_image_url(ndvi, geometry, ndvi_vis_params)
        ndmi_url = get_image_url(ndmi, geometry, ndmi_vis_params)
        ndwi_url = get_image_url(ndwi, geometry, ndwi_vis_params)

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
        farm.ndwi_path = os.path.join('generated/ndwi_images', f'{farm.id}_ndwi.png')
        farm.save()
    except Exception as e:
        print(f"Error downloading satellite image: {e}")


def get_time_series(geometry, start_date, end_date, indices = ["NDWI", "MDMI", "NDWI"], interval = "month"):
    """
    Retrieves a time series of vegetation indices for a given area and time period.

    This function retrieves a collection of Landsat 8 images for the specified 
    geometry and date range, filters for images with less than 5% cloud cover, 
    calculates the requested vegetation indices (NDVI, NDMI, and optionally others), 
    reduces the data to mean values over a specified interval (month by default), 
    and returns a list of dictionaries containing the date and corresponding 
    mean values for each requested index.

    Args:
        geometry: An Earth Engine geometry object representing the area of interest.
        start_date: A string representing the start date in YYYY-MM-DD format.
        end_date: A string representing the end date in YYYY-MM-DD format.
        indices (optional): A list of strings representing the desired vegetation indices 
                            (default: ["NDVI", "MDMI", "NDWI"]).
        interval (optional): A string representing the time interval for averaging 
                            data (default: "month"). Valid options include "year", 
                            "quarter", and "month".

    Returns:
        A list of dictionaries, where each dictionary contains:
            - "date": The date of the image (string in YYYY-MM-DD format).
            - "NDVI": The mean NDVI value for the specified interval (float, or None 
                        if no data available).
            - "NDMI": The mean NDMI value for the specified interval (float, or None 
                        if no data available).
            - "MDMI" (optional): The mean MDMI value for the specified interval 
                        (float, or None if not requested or no data available).
            - Additional index keys can be included based on the `indices` argument.
    """
    collection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
            .filterBounds(geometry) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', 5))
    
    def compute_index(image):
        ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
        ndmi = image.normalizedDifference(["B8", "B11"]).rename("NDMI")
        ndwi = image.normalizedDifference(["B3", "B8"]).rename("NDWI")
        return image.addBands([ndvi, ndmi, ndwi])
    
    collection = collection.map(compute_index)

    def reduce_over_time(image):
        stats = image.reduceRegion(
            reducer = ee.Reducer.mean(),
            geometry = geometry,
            scale = 10,
            bestEffort = True
        )
        return image.set("date", image.date().format()).set("stats", stats)

    reduced_collection = collection.map(reduce_over_time)

    # Get time series as a list of dictionary
    time_series = reduced_collection.aggregate_array("stats").getInfo()
    dates = reduced_collection.aggregate_array("date").getInfo()

    result = []
    for i in range(len(time_series)):
        data = time_series[i]
        if data:
            result.append({
                "date": dates[i],
                "NDVI": data.get("NDVI", None),
                "NDMI": data.get("NDMI", None),
                "NDWI": data.get("NDWI", None),
            })

    return result



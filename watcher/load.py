from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import farm

farm_mapping = {
    "fid": "fid",
    "name": "Name",
    "size": "Size",
    "crop": "Crop",
    "geom": "MULTIPOLYGON",
}

farm_shp = Path(__file__).resolve().parent / "data" / "KBFarmlands.shp"

def run(verbose = True):
    lm = LayerMapping(farm, farm_shp, farm_mapping, transform = False)
    lm.save(strict = True, verbose = verbose)
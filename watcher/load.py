from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import watcher_model

watcher_mapping = {
    "fid": "fid",
    "name": "Name",
    "size": "Size",
    "crop": "Crop",
    "geom": "MULTIPOLYGON",
}

watcher_shp = Path(__file__).resolve().parent / "data" / "KBFarmlands.shp"

def run(verbose = True):
    lm = LayerMapping(watcher_model, watcher_shp, watcher_mapping, transform = False)
    lm.save(strict = True, verbose = verbose)
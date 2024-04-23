from pathlib import path
from pathlib import Path
from django.contrib.gis.gdal import DataSource
import watcher

watcher_shp = Path(watcher.__file__).resolve().parent / "data" / "KBFarmlands.shp"
ds = DataSource(watcher_shp)
print(ds)
print(len(ds))
lyr = ds[0]
print(lyr)
print(lyr.geom_type)
print(len(lyr))
print(lyr.srs)
print(lyr.fields)

for feat in lyr:
    print(feat.get("NAME"), feat.geom.num_points)
feat = lyr[234]
print(feat.get("NAME"))

geom = feat.geom
print(geom.wkt)
print(geom.json)
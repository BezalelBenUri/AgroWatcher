from django.contrib.gis.db import models

# Create your models here.
class farm(models.Model):
    fid = models.FloatField()
    name = models.CharField(max_length = 50)
    size = models.FloatField()
    crop = models.CharField(max_length = 10)

    geom = models.MultiPolygonField(srid = 4326)
    image_path = models.CharField(max_length = 255, blank = True, null = True)
    ndvi_path = models.CharField(max_length = 255, blank = True, null = True)
    ndmi_path = models.CharField(max_length = 255, blank = True, null = True)
    ndwi_path = models.CharField(max_length = 255, blank = True, null = True)

    def __str__(self):
        return self.name
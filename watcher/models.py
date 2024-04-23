from django.contrib.gis.db import models

# Create your models here.
class watcher_model(models.Model):
    fid = models.FloatField()
    name = models.CharField(max_length = 50)
    size = models.FloatField()
    crop = models.CharField(max_length = 10)

    geom = models.MultiPolygonField(srid = 4326)

    def __str__(self):
        return self.name
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField
from .models import watcher_model

class farmSerializer(GeoFeatureModelSerializer):
    geom = GeometryField()

    class  Meta:
        model = watcher_model
        geo_field = "geom"
        fields = "__all__"
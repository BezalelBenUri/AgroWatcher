from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField
from .models import farm

class farmSerializer(GeoFeatureModelSerializer):
    geom = GeometryField()

    class  Meta:
        model = farm
        geo_field = "geom"
        fields = "__all__"
from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework_gis.fields import GeometryField


class GeometrySerializer(serializers.Serializer):
    geom = GeometryField()
    srid = IntegerField()

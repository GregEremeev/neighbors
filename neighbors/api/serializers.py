from drf_extra_fields.geo_fields import PointField
from rest_framework.fields import IntegerField, FloatField
from rest_framework.serializers import ModelSerializer, Serializer

from neighbors.core.models import User


class NearestNeighborsQueryParams(Serializer):

    limit = IntegerField(max_value=100, min_value=1)
    radius = FloatField(max_value=1000, min_value=1)


class UserSerializer(ModelSerializer):

    location = PointField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'location')

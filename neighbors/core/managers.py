from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.auth.models import UserManager
from django.contrib.gis.db.models import GeoManager


class UserManager(UserManager, GeoManager):

    def filter_nearest(self, location, radius):
        point = Point(location.coords)
        return self.filter(location__dwithin=(point, D(km=radius))).distance(point).order_by('distance')

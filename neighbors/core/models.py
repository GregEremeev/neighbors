from neighbors.core.managers import UserManager
from django.contrib.gis.db.models import PointField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    location = PointField(geography=True, srid=4326)

    objects = UserManager()

    def get_nearest_users(self, radius, limit):
        qs = self._meta.model.objects.filter_nearest(self.location, radius).exclude(id=self.id)
        return list(qs[:limit])

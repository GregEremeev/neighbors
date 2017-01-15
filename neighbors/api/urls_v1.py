from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from neighbors.api.views import UserViewSet


user_router = DefaultRouter()
user_router.register('users', UserViewSet)


urlpatterns = [
    url('', include(user_router.urls)),
]

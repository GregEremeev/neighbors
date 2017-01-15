from django.conf.urls import url, include

from neighbors.api import urls_v1


urlpatterns = [
    url(r'^v1/', include(urls_v1, namespace='v1')),
]

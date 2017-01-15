from django.conf.urls import include, url


urlpatterns = [
    url(r'^api/', include('neighbors.api.urls')),
]

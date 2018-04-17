from django.conf.urls import url
from .views import recording


urlpatterns = [
    url(r'^recording/$', recording, name='recording'),
]
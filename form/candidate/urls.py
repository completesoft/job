from django.conf.urls import url
from . import views

app_name = 'candidate'
urlpatterns = [
    url(r'^(?P<loc_id>\w+)/$', views.person, name='index'),
    url(r'^check/$', views.server_response, name='server_response'),
]


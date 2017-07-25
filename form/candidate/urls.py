from django.conf.urls import url
from . import views

app_name = 'candidate'
urlpatterns = [
    url(r'^$', views.person, name='index'),
    url(r'^check/$', views.server_response, name='server_response'),
]


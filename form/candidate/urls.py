from django.conf.urls import url
from . import views

app_name = 'candidate'
urlpatterns = [
    url(r'^$', views.person, name='index'),
    url(r'^thanks', views.thanks, name='thanks')
]


from django.conf.urls import url
from .views import CvList, CvDetail, CvUpdate

app_name = 'cv_manager'

urlpatterns = [
    url(r'^$', CvList.as_view(), name="cv_list"),
    url(r'^detail/(?P<person_id>\d+)/$', CvDetail.as_view(), name="cv_detail"),
    url(r'^update/(?P<person_id>\d+)/$', CvUpdate.as_view(), name="cv_update"),
]
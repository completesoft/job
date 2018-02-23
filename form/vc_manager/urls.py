from django.conf.urls import url
from .views import VcList, VcDetail, VcUpdate

app_name = 'vc_manager'

urlpatterns = [
    url(r'^$', VcList.as_view(), name="vc_list"),
    url(r'^detail/(?P<person_id>\d+)/$', VcDetail.as_view(), name="vc_detail"),
    url(r'^update/(?P<person_id>\d+)/$', VcUpdate.as_view(), name="vc_update"),
]
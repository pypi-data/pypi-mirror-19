from django.conf.urls import url

from utm_zone_info import views

urlpatterns = [
    url(r'^utm-zone-info/$', views.utm_zone_info, name='utm-zone-info'),
]

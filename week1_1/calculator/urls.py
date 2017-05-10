from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'add/([0-9]+)/([0-9]+)/$', views.sum),
    url(r'multiply/([0-9]+)/([0-9]+)/$', views.multiply),
    url(r'power/([0-9]+)/([0-9]+)/$', views.power),
    url(r'fact/([0-9]+)/$', views.fact),
]

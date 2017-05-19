from django.conf.urls import url

from . import views


urlpatterns = [
    url('^$', views.index, name='index_url'),
    url('^thanks/$', views.thanks, name='thanks_url'),
]

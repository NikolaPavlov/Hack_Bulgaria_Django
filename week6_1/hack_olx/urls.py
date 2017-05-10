from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index_url'),
    url(r'^login/$', views.login_view, name='login_url'),
    url(r'^logout/$', views.logout_view, name='logout_url'),
    url(r'^register/$', views.register, name='register_url'),

    url(r'^add_offer/$', views.add_offer, name='add_offer_url'),
    url(r'^statistics/$', views.statistics, name='statistics_url'),
]

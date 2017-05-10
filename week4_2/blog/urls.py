from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index_url'),
    url(r'^login/$', views.login_view, name='login_url'),
    url(r'^logout/$', views.logout_view, name='logout_url'),
    url(r'^profile/$', views.profile_view, name='profile_url'),

    url(r'^detail/([0-9]+)/$', views.detail_post_view, name='detail_url'),
    url(r'^create_post/$', views.create_post, name='create_post'),
]

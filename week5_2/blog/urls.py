from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index_url'),
    url(r'^login/$', views.login_view, name='login_url'),
    url(r'^logout/$', views.logout_view, name='logout_url'),
    url(r'^register/$', views.register_view, name='register_url'),

    url(r'^detail/([0-9]+)/$', views.detail_post_view, name='detail_url'),
    url(r'^create_blog_post/$', views.create_blog_post, name='create_blog_post_url')
]

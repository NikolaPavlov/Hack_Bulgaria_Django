from django.conf.urls import url
from . import views


urlpatterns = [
    url('^$', views.index),
    url('detail/(?P<post_id>[0-9])', views.detail, name='detail_url'),
    url('create-post/$', views.blog_post_create, name='create_post_url'),
]

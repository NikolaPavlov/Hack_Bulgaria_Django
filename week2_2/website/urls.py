from django.conf.urls import url
from . import views


uuid_regex = '([a-zA-Z]|[0-9]){8}\-([a-zA-Z]|[0-9]){4}\-([a-zA-Z]|[0-9]){4}\-([a-zA-Z]|[0-9]){4}\-([a-zA-Z]|[0-9]){12}'
urlpatterns = [
    url(r'user-detail/(?P<identifier>{})/$'.format(uuid_regex), views.detail_view, name='user_detail'),
    url(r'add-key/(?P<identifier>{})/$'.format(uuid_regex), views.add_key, name='add_key'),
    url(r'^$', views.index),
]

from django.conf.urls import url

from .views import create_user_view, manage_key_view, set_key_view


uuid_regex = '([a-zA-Z]|[0-9]){8}\-([a-zA-Z]|[0-9]){4}\-([a-zA-Z]|[0-9]){4}\-([a-zA-Z]|[0-9]){4}\-([a-zA-Z]|[0-9]){12}'
urlpatterns = [
    url(r'^create-user/$', create_user_view),
    url(r'(?P<identifier>{})/$'.format(uuid_regex), set_key_view),
    url(r'(?P<identifier>{})/(?P<key>[a-zA-Z0-9]+)/$'.format(uuid_regex), manage_key_view),
]

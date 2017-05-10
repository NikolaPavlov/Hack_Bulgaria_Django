from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^api/$', views.OfferList.as_view()),
    url(r'^api/(?P<pk>[0-9+])/$', views.OfferDetail.as_view()),
]

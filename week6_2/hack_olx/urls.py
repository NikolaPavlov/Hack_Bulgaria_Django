from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.OfferListView.as_view(), name='index_url'),
    url(r'^login/$', views.login_view, name='login_url'),
    url(r'^logout/$', views.logout_view, name='logout_url'),
    url(r'^register/$', views.register, name='register_url'),

    url(r'^add_offer/$', views.OfferCreateView.as_view(), name='add_offer_url'),
    url(r'^offers_by_category/cat/(?P<pk>[0-9]+)/$',
        views.OffersByCategoryView.as_view(), name='offers_by_category_url'),
    url(r'^offer/(?P<pk>[0-9]+)/$', views.OfferDetailView.as_view(), name='offer_detail_url'),
    url(r'^offer/edit/(?P<pk>[0-9]+)/$', views.UpdateOfferView.as_view(), name='offer_edit_url'),
    url(r'^statistics/$', views.StatisticTemplateView.as_view(), name='statistics_url'),
]

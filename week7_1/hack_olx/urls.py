from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.OffersIndexView.as_view(), name='index_url'),
    url(r'^login/$', views.login_view, name='login_url'),
    url(r'^logout/$', views.logout_view, name='logout_url'),
    url(r'^register/$', views.register, name='register_url'),

    url(r'^approved_and_rejected/$',
        views.ApprovedAndRejectedOffes.as_view(),
        name='approve_and_rejected_url'),

    url(r'^add_offer/$',
        views.OfferCreateView.as_view(),
        name='add_offer_url'),

    url(r'^offer/(?P<pk>[0-9]+)/$',
        views.OfferDetailView.as_view(),
        name='offer_detail_url'),

    url(r'^offer/edit/(?P<pk>[0-9]+)/$',
        views.UpdateOfferView.as_view(),
        name='offer_edit_url'),

    url(r'^offer/delete/(?P<pk>[0-9]+)/$',
        views.DeleteOfferView.as_view(),
        name='delete_offer_url'),

    url(r'^offer/approve/(?P<pk>[0-9]+)/$',
        views.offer_approve,
        name='approve_offer_url'),

    url(r'^offer/reject/(?P<pk>[0-9]+)/$',
        views.offer_reject,
        name='reject_offer_url'),

    url(r'^offers_by_category/(?P<pk>[0-9]+)/$',
        views.OffersByCategoryView.as_view(),
        name='offers_by_category_url'),

    url(r'^pending_offers/$',
        views.OfferPendingListView.as_view(),
        name='pending_offers_url'),

    url(r'^statistics/$',
        views.StatisticTemplateView.as_view(),
        name='statistics_url'),
]

from django.conf.urls import url

from oscar_wagtail import views

urlpatterns = [
    url(r'^product-choose/$',
        views.product_choose, name='product_choose'),

    url(r'^product-choose/(\d+)/$',
        views.product_chosen, name='product_chosen'),

    url(r'^offer-choose/$',
        views.offer_choose, name='offer_choose'),

    url(r'^offer-choose/(\d+)/$',
        views.offer_chosen, name='offer_chosen'),
]

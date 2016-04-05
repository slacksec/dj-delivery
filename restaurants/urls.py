from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet)

router.urls.extend([
    url(r'^restaurants/(?P<slug>[\w-]+)/hours/$',
        views.OpenHoursList.as_view(),
        name='open-hours'),
    url(r'^restaurants/(?P<slug>[\w-]+)/menu/$',
        views.MenuList.as_view(),
        name='menu-item-list'),
    url(r'^restaurants/(?P<slug>[\w-]+)/menu/(?P<pk>\d+)/$',
        views.MenuDetail.as_view(),
        name='menu-item-detail')
])
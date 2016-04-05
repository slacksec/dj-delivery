from django.conf.urls import url, include

from restaurants.urls import router

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^', include('frontend.urls')),
]

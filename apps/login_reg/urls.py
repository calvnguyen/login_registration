from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^success$', views.show),
    url(r'^register$', views.create_user),
    url(r'^logout$', views.logout)
]

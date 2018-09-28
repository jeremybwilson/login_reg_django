from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^new$', views.new, name="new"),
    url(r'^create$', views.create, name="create"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^success$', views.success, name="success"),
    url(r'^(?P<user_id>\d+)/show$', views.show, name="show"),
    url(r'^(?P<user_id>\d+)/delete$', views.delete, name="delete"),
]
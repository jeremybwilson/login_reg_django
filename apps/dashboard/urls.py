from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^process$', views.process, name="process"),
    url(r'^show$', views.show, name="show"),
    url(r'^reset$', views.reset, name="reset"),
]
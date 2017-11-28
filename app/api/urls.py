from django.conf.urls import url

from . import apiViews

urlpatterns = [
    url(r'^', apiViews.index, name='index'),
]
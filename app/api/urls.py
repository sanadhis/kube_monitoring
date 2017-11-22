from django.conf.urls import url

from . import newViews

urlpatterns = [
    url(r'^', newViews.index, name='index'),
]
from django.conf.urls import url

from . import apiViews

urlpatterns = [
    url(r'^', apiViews.main, name='main'),    # all pattern goes to main function
]
from django.conf.urls import url

from . import views, authentication

urlpatterns = [
    url(r'^login/', views.render_login, name='login'),
    url(r'^stats/', views.index, name='index'),
    url(r'^authentication/signin', authentication.signin, name='signin'),
    url(r'^authentication/signout', authentication.signout, name='signout'),    
    url(r'^$', views.index, name='index'),    
]
from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views, authentication

# default url pattern -> /web/stats/index
# without login       -> /web/login/
urlpatterns = [
    url(r'^login/', views.render_login, name='login'),
    url(r'^login', RedirectView.as_view(url='login/', permanent=False), name='login'),    
    url(r'^stats/', views.index, name='index'),
    url(r'^stats', RedirectView.as_view(url='stats/', permanent=False), name='index'),    
    url(r'^authentication/signin', authentication.signin, name='signin'),
    url(r'^authentication/signout', authentication.signout, name='signout'),
    url(r'^$', RedirectView.as_view(url='stats/', permanent=False), name='index'),
]
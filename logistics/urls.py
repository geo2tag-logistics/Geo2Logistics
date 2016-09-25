from django.conf.urls import *

from logistics.views import home

urlpatterns = [
    url(r'^', home, name='home'),
]
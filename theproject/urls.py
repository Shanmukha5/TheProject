from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^company/', include('company.urls')),
    url(r'^worker/', include('worker.urls')),
    url(r'^panel/', include('panel.urls')),
    url(r'^myprofile/(?P<uid>\w+)/$', views.profiledisplay),
]

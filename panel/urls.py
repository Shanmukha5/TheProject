from django.conf.urls import url
from . import views





urlpatterns = [
	url(r'^$', views.home),
	url(r'^signin/$', views.signin),
	url(r'^signin/submit/$', views.signinsubmit),
	url(r'^logout/$', views.logout),
	url(r'^(?P<workeruid>\w+)/$', views.showingworkerdetails),
	url(r'^(?P<workeruid>\w+)/ratingsubmit/$', views.ratingsubmit),
	
]
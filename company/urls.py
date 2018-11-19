from django.conf.urls import url, include
from . import views as companyviews


urlpatterns = [
	url(r'^$', companyviews.home),
	url(r'^signup/$', companyviews.signup),
	url(r'^signup/submit/$', companyviews.signupsubmit),
	url(r'^signin/$', companyviews.signin),
	url(r'^signin/submit/$', companyviews.signinsubmit),
	url(r'^submitdoc/$', companyviews.submitdoc),
	url(r'^submitdoc/submit$', companyviews.submitdocsubmit),
	url(r'^logout/$', companyviews.logout),
	url(r'^editprofile/$', companyviews.editprofile),
	url(r'^editprofile/submit/$', companyviews.editprofilesubmit),
	url(r'^status/$', companyviews.status),
	url(r'^skillqueryregex/$', companyviews.skillqueryregex),
	url(r'^query_(?P<skillquery>\w+)/$', companyviews.skillquery),
	url(r'^(?P<uid>\w+)/hire/$', companyviews.hire),
	url(r'^(?P<uid>\w+)/agreement/$', companyviews.agreement),
	url(r'^seeresults/$', companyviews.seeresults),
	url(r'myprofile/(?P<uid>\w+)/$', companyviews.profile),
]





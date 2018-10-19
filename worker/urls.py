from django.conf.urls import url, include
from . import views


urlpatterns = [
	url(r'^$', views.home, name='workerhome'),
	url(r'^signup/$', views.signup, name='workersignup'),
	url(r'^signup/submit/$', views.signupsubmit, name='workersignupsubmit'),
	url(r'^signin/$', views.signin),
	url(r'^signin/submit/$',views.signinsubmit),
	url(r'^submitdoc/$', views.submitdoc),
	url(r'^submitdoc/submit/$', views.submitdocsubmit),
	url(r'^addcertificates/$', views.addcertificates),
	url(r'^addcertificates/submit/$', views.addcertificatessubmit),
	url(r'^logout/$', views.logout),
	url(r'^editprofile/$', views.editprofile),
	url(r'^editprofile/submit/$', views.editprofilesubmit),
	url(r'^status/$', views.status),
	url(r'^questionnaire/$', views.questionnaire),
	url(r'^questionnaire/java/$', views.questionnairejava),
	url(r'^questionnaire/python/$', views.questionnairepython),
	url(r'^questionnaire/marketing/$', views.questionnairemarketing),
	url(r'^questionnaire/webdesigner/$', views.questionnairewebdesigner),
	url(r'^questionnaire/java/submit/$', views.questionnairejavasubmit),
	url(r'^questionnaire/python/submit/$', views.questionnairepythonsubmit),
	url(r'^questionnaire/marketing/submit/$', views.questionnairemarketingsubmit),
	url(r'^questionnaire/webdesigner/submit/$', views.questionnairewebdesignersubmit),

	url(r'^seeresults/$', views.seeresults),

	url(r'^count/$', views.count),
]
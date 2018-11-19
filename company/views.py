from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import pyrebase
from django.contrib import auth
import numpy
from panel.models import workerdetails
from django.core import serializers


config = {
    "apiKey": "AIzaSyD7MVWjMWPnyguId_WKdJueN1TMK-8kkc4",
    "authDomain": "the-project-6ca2f.firebaseapp.com",
    "databaseURL": "https://the-project-6ca2f.firebaseio.com",
    "projectId": "the-project-6ca2f",
    "storageBucket": "the-project-6ca2f.appspot.com",
    "messagingSenderId": "28467301382"
  }

firebase= pyrebase.initialize_app(config)

firebaseauth = firebase.auth()

database = firebase.database()

def home(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users']
		a = a[0]
		a = a['localId']
		details = database.child('users').child("Company").child(a).child('details').child('name').get().val()
		pythondata = workerdetails.objects.filter(skill='Python').order_by('rating')[:2].values()
		javadata = workerdetails.objects.filter(skill='Java').order_by('rating')[:2]
		marketingdata = workerdetails.objects.filter(skill='Marketing').order_by('rating')[:2]
		webdesignerdata = workerdetails.objects.filter(skill='WedDesigner').order_by('rating')[:2]
		return render(request,'company/home.html', {'details': details,'pythondata': pythondata, 'javadata':javadata, 'marketingdata': marketingdata, 'webdesignerdata':webdesignerdata})
	except Exception as ex:
		return HttpResponse(ex)
		message = None
		detials = None
		return render(request, 'company/home.html',{'msg': message})


def signup(request):
	message = None
	return render(request, 'company/signup.html',{'msg':message})


def signupsubmit(request):
	name = request.POST.get('name')
	email = request.POST.get('email')
	password = request.POST.get('password')
	try:
		user = firebaseauth.create_user_with_email_and_password(email, password)
	except Exception as ex:
		message = "Unable to create account. Try again"
		print(ex)
		return render(request, 'company/home.html',{'msg':message})
	uid = user['localId']
	data = {
		'name':name,
		'email':email,
	}
	verfication = {
		'verfication': "Not yet Verified!"
	}
	database.child("users").child('Company').child(uid).child('details').set(data)
	database.child('users').child('Company').child(uid).child('verfication').set(verfication)
	database.child('users').child('Company').child(uid).child('notifications').child('notificationcount').child('count').set(0)
	message = "Your account has created successfully. Now Sign in."
	return render(request, 'company/signup.html',{'msg':message})


def signin(request):
	details = None
	return render(request, 'company/signin.html')

def signinsubmit(request):
	email = request.POST.get('email')
	password = request.POST.get('password')
	try:
		user = firebaseauth.sign_in_with_email_and_password(email, password)
	except:
		message = "Invalid Credentials"
		return render(request, 'company/home.html',{'msg':message})
	session_id = user['idToken']
	request.session['uid'] = str(session_id)
	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	b = a['users'][0]['localId']
	data = database.child('users').child('Company').child(b).child('details').child('name').get().val()
	message = "Your are logged in successfully"
	return render(request, 'company/home.html',{"details":data,"msg":message})




def logout(request):
	auth.logout(request)
	return redirect(home)



def submitdoc(request):
	a = None
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users']
		a = a[0]
		a = a['localId']
	except Exception as ex:
		a = str(ex)
		if "INVALID_ID_TOKEN" in a:
			return HttpResponse("User Not logged In")
	return render(request, 'company/submitdoc.html')

def submitdocsubmit(request):
	url = request.POST.get('url')
	firstname = request.POST.get('firstname')
	lastname = request.POST.get('lastname')
	companyname = request.POST.get('companyname')
	jobrole = request.POST.get('jobrole')
	officialmail = request.POST.get('officialmail')
	websiteurl = request.POST.get('websiteurl')
	phonenumber = request.POST.get('phonenumber')
	gstcode = request.POST.get('gstcode')

	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	a = a['users']
	a = a[0]
	a = a['localId']
	data = {
		'firstname':firstname,
		'lastname': lastname,
		'companyname': companyname,
		'jobrole': jobrole,
		'officialmail': officialmail,
		'websiteurl': websiteurl,
		'phonenumber': phonenumber,
		'gstcode': gstcode,
		'url':url,
	}
	abc = database.child('users').child("Company").child(a).child('profile').set(data)
	return HttpResponse(abc)





def editprofile(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users']
		a = a[0]
		a = a['localId']
		try:
			editdetails = database.child('users').child("Company").child(a).child('profile').shallow().get().val()
		except:
			return HttpResponse("You haven't submitted your profile yet!")
		firstname = database.child('users').child('Company').child(a).child('profile').child('firstname').get().val()
		lastname = database.child('users').child('Company').child(a).child('profile').child('lastname').get().val()
		companyname = database.child('users').child('Company').child(a).child('profile').child('companyname').get().val()
		jobrole = database.child('users').child('Company').child(a).child('profile').child('jobrole').get().val()
		officialmail = database.child('users').child('Company').child(a).child('profile').child('officialmail').get().val()
		websiteurl = database.child('users').child('Company').child(a).child('profile').child('websiteurl').get().val()
		phonenumber = database.child('users').child('Company').child(a).child('profile').child('phonenumber').get().val()
		gstcode = database.child('users').child('Company').child(a).child('profile').child('gstcode').get().val()
		name = database.child('users').child('Company').child(a).child('details').child('name').get().val()
		return render(request,'company/editprofile.html', {'firstname':firstname, 'lastname': lastname,'phonenumber': phonenumber, 'jobrole': jobrole, 'companyname':companyname, 'officialmail':officialmail, 'websiteurl': websiteurl, 'gstcode': gstcode, 'name': name})
	except:
		return render(request, 'company/editprofile.html')


def editprofilesubmit(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	firstname = request.POST.get('firstname')
	lastname = request.POST.get('lastname')
	companyname = request.POST.get('companyname')
	jobrole = request.POST.get('jobrole')
	officialmail = request.POST.get('officialmail')
	websiteurl = request.POST.get('websiteurl')
	phonenumber = request.POST.get('phonenumber')
	gstcode = request.POST.get('gstcode')
	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	a = a['users'][0]['localId']
	data = {
		'firstname': firstname,
		'lastname': lastname,
		'companyname': companyname,
		'jobrole': jobrole,
		'officialmail': officialmail,
		'websiteurl': websiteurl,
		'phonenumber': phonenumber,
		'gstcode': gstcode
	}
	database.child('users').child('Company').child(a).child('profile').set(data)
	return HttpResponse("Profile Updated")


def status(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	status = database.child('users').child('Company').child(a).child('verfication').child('verfication').get().val()
	return render(request, 'company/status.html', {'status': status})


def skillquery(request, skillquery):
	data = workerdetails.objects.filter(skill=skillquery).order_by('rating')
	return HttpResponse(data)

def skillqueryregex(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")


	search = request.POST.get('searchquery')
	data = workerdetails.objects.order_by('rating').filter(description__icontains=search).values()
	return render(request, 'company/regexquery.html',{'querylist':data})



def hire(request, uid):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	try:
		skill = request.POST.get('skill')
		month = request.POST.get('month')
		companyname = database.child('users').child('Company').child(a).child('profile').child('companyname').get().val()
		workername = database.child('users').child('worker').child(uid).child('profile').get().val()
		"""
		count = database.child('users').child('worker').child(uid).child('notifications').child('notificationcount').child('count').get().val()
		newnotification = "notification"+str(count)
		companyname = database.child('users').child('Company').child(a).child('profile').child('companyname').get().val()
		companylink = "127.0.1:8000/companyprofile/"+str(a)+"/"
		database.child('users').child('worker').child(uid).child('notifications').child(newnotification).child("notification").set(companyname+" wants to hire you")
		workername = database.child('users').child('worker').child(uid).child('profile').get().val()
		companynotificationcount = database.child('users').child("Company").child(a).child('notifications').child('notificationcount').child('count').get().val()
		companynewnotification = "notification"+str(companynotificationcount)
		workerlink = "127.0.1:8000/companyprofile/"+str(uid)+"/"
		database.child('users').child('Company').child(a).child('notifications').child(companynewnotification).child('notification').set("You sent hiring request to "+workername+" for "+month+" months, skill "+ skill)
		"""
		return render(request, 'company/agreement.html', {'workername': workername, 'companyname': companyname, 'month': month, 'skill':skill, 'uid':uid})
	except:
		return HttpResponse("Hiring process interrupted")
	return HttpResponse("You are hiring "+uid)

def agreement(request, uid):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	agreementsubmission = request.POST.get('agreementsubmission')
	time = request.POST.get('time')
	skill = request.POST.get('skill')
	if(agreementsubmission=='Request'):
		try:
			count = database.child('users').child('worker').child(uid).child('notifications').child('notificationcount').child('count').get().val()
			newnotification = "notification"+str(count)
			companyname = database.child('users').child('Company').child(a).child('profile').child('companyname').get().val()
			companylink = "127.0.1:8000/worker/myprofile/"+str(a)+"/"+str(count)+"/"
			database.child('users').child('worker').child(uid).child('notifications').child(newnotification).child("notification").set(companyname+" wants to hire you")
			database.child('users').child('worker').child(uid).child('notifications').child(newnotification).child("companyprofilelink").set(companylink)
			database.child('users').child('worker').child(uid).child('notifications').child(newnotification).child('companyname').set(companyname)
			database.child('users').child('worker').child(uid).child("notifications").child(newnotification).child('skill').set(skill)
			database.child('users').child('worker').child(uid).child("notifications").child(newnotification).child('time').set(time)
			workername = database.child('users').child('worker').child(uid).child('profile').get().val()
			try:
				companynotificationcount = database.child('users').child("Company").child(a).child('notifications').child('notificationcount').child('count').get().val()
				if(companynotificationcount==None):
					companynotificationcount = 0
			except:
				companynotificationcount = 0
			companynewnotification = "notification"+str(companynotificationcount)
			workerlink = "127.0.1:8000/company/myprofile/"+str(uid)+"/"+str(companynotificationcount)+"/"
			text = "You sent hiring request to "+str(workername)
			database.child('users').child('Company').child(a).child('notifications').child(companynewnotification).child('notification').set(text)
			database.child('users').child("Company").child(a).child('notifications').child(companynewnotification).child('workerprofilelink').set(workerlink)
			database.child('users').child('Company').child(a).child('notifications').child(companynewnotification).child('workername').set(workername)
			database.child('users').child('Company').child(a).child('notifications').child(companynewnotification).child('time').set(time)
			database.child('users').child('Company').child(a).child('notifications').child(companynewnotification).child('skill').set(skill)
			database.child('users').child('Company').child(a).child('notifications').child('notificationcount').set(companynotificationcount+1)
			return HttpResponse("You hiring message sent successfully")
		except Exception as ex:
			return HttpResponse(ex)
			return HttpResponse("Agreement unsuccessful")
	else:
		return HttpResponse("Your declined the process")
	

def profile(request, uid):
	#show the details of the company to worker
	return HttpResponse(uid)




def seeresults(request):
	return render(request,'company/seeresults.html')

#Checking view for just to check the new implementation techniques

def checking(request):
	return HttpResponse("Checking Point")
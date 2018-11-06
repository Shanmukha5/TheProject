from django.shortcuts import render, HttpResponse, redirect
import pyrebase
from django.contrib import auth




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
		email = database.child('users').child('panel').child(a).child('details').child('email').child('email').get().val()
		data = database.child('users').child('worker').shallow().get().val()
		skill = database.child('users').child('panel').child(a).child('details').child('skill').child('skill').get().val()
		list =[]
		uidlist = []
		for i in data:
			if(database.child('users').child('worker').child(i).child('verfication').child('verfication').get().val()=='Under verification'):
				if(database.child('users').child('worker').child(i).child('verifiedby').child(skill).child('email').get().val()==database.child('users').child('panel').child(a).child('details').child('email').child('email').get().val()):
					list.append(database.child('users').child('worker').child(i).child('details').child('name').get().val())
					uidlist.append(i)
		return render(request, 'panel/home.html', {'email':email, 'data':list, 'uidlist': uidlist})
	except:
		return HttpResponse("Not signed in")
		return render(request, 'panel/home.html')


def signin(request):
	return render(request, 'panel/signin.html')


def signinsubmit(request):
	email = request.POST.get('email')
	password = request.POST.get('password')
	try: 
		user = firebaseauth.sign_in_with_email_and_password(email, password)
	except Exception as ex:
		message = "Invalid Credentials"
		return render(request, 'panel/signin.html',{'msg':message})
	session_id = user['idToken']
	request.session['uid'] = str(session_id)
	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	b = a['users'][0]['localId']
	data = {
		'email' : email,
	}
	data = database.child('users').child('panel').child(b).child('details').child('email').set(data)
	return render(request, 'panel/home.html', {'email':email})

def showingworkerdetails(request, workeruid):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	paneluids = database.child('users').child('panel').get().val()
	mail = database.child('users').child('panel').child(a).child('details').child('email').child('email').get().val()
	workeruids = database.child('users').child('worker').get().val()
	skill = database.child('users').child('panel').child(a).child('details').child('skill').child('skill').get().val()
	if(a in paneluids):
		if(workeruid in workeruids):
			if(database.child('users').child('worker').child(workeruid).child('verifiedby').child(skill).child('email').get().val()==mail):
				workername = database.child('users').child('worker').child(workeruid).child('details').child('name').get().val()
				certificates = database.child('users').child('worker').child(workeruid).child('certificates').child(skill).get().val()
				certificateslist = []
				for i in certificates:
					certificateslist.append(database.child('users').child('worker').child(workeruid).child('certificates').child(skill).child(i).get().val())
				questionnaire = database.child('users').child('worker').child(workeruid).child('questionnaire').child(skill).get().val()
				questionnairelist = []
				for i in questionnaire:
					questionnairelist.append(database.child('users').child('worker').child(workeruid).child('questionnaire').child(skill).child(i).get().val())
				return render(request, 'panel/workerdetails.html', {'workername':workername,'certificates': certificateslist, 'questionnaire': questionnairelist, 'uid':workeruid})			
			else:
				return HttpResponse("Something")
		else:
			return HttpResponse("No user with that url")
	return HttpResponse("You are not panel")

#rating should be changed to Java verification and make changes according to it
def ratingsubmit(request, workeruid):	
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	paneluids = database.child('users').child('panel').get().val()
	workeruids = database.child('users').child('worker').get().val()
	skill = database.child('users').child('panel').child(a).child('details').child('skill').child('skill').get().val()
	if(a in paneluids):
		if(workeruid in workeruids):
			rating = request.POST.get('rating')
			verification = request.POST.get('verificationbutton')
			database.child('users').child('worker').child(workeruid).child('verfication').child('verfication').set(verification)
			database.child('users').child('worker').child(workeruid).child('rating').child(skill).child('rating').set(rating)
			return HttpResponse("You have rated the employee successfully")
		else:
			return HttpResponse("No user found with that url")

	return HttpResponse("Done")




def logout(request):
	auth.logout(request)
	return redirect(home)



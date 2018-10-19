from django.shortcuts import render, HttpResponse
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
		email = database.child('users').child('panel').child(a).child('details').child('email').get().val()
		data = database.child('users').child('worker').shallow().get().val()
		list =[]
		for i in data:
			if(database.child('users').child('worker').child(i).child('verfication').child('verfication').get().val()=='Under verification'):
				list.append(database.child('users').child('worker').child(i).child('details').child('name').get().val())
		return render(request, 'panel/home.html', {'email':email, 'data':list})
	except:
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
	data = database.child('users').child('panel').child(b).child('details').set(data)
	return render(request, 'panel/home.html', {'email':email})
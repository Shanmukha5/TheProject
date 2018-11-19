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
	return render(request, 'home.html')


def profiledisplay(request, uid):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	paneluids = database.child('users').child('panel').shallow().get().val()
	workeruids = database.child('users').child('worker').shallow().get().val()
	companyuids = database.child('users').child('Company').shallow().get().val()
	if(a in workeruids or paneluids or companyuids):
		if(uid in workeruids):
			profile = database.child('users').child('worker').child(uid).child('profile').get().val()
			skills = database.child('users').child('worker').child(uid).child('rating').get().val()
			ratinglist = []
			for i in skills:
				ratinglist.append(database.child('users').child('worker').child(uid).child('rating').child(i).child('rating').get().val())
			data = zip(skills,ratinglist)
			return render(request, 'workerprofile.html', {'profile': profile, 'data': data,'uid':uid})
			return HttpResponse(profile)
	else:
		return HttpResponse("No user found with that url")

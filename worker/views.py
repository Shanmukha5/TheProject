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
		details = database.child('users').child("worker").child(a).child('details').child('name').get().val()
		companies = database.child('users').child('Company').get().val()
		companiesdict = {}
		profilename = None
		profilephonenumber = None
		profilepic = None
		if(database.child('users').child('worker').child(a).child('profile').get().val()!=None):
			profilename = str(database.child('users').child('worker').child(a).child('profile').child('firstname').get().val()) + str(database.child('users').child('worker').child(a).child('profile').child('lastname').get().val())
			profilephonenumber = database.child('users').child('worker').child(a).child('profile').child('phonenumber').get().val()
			profilepic = database.child('users').child('worker').child(a).child('profile').child('url').get().val()
		for i in companies:
			companiesdict[database.child('users').child('Company').child(i).child('profile').child('companyname').get().val()] = {}
			companiesdict[database.child('users').child('Company').child(i).child('profile').child('companyname').get().val()]['officialmail'] = database.child('users').child('Company').child(i).child('profile').child('officialmail').get().val()
			#show officialmail and url
		return render(request,'worker/home.html', {'details': details, 'companies': companiesdict, 'profilename': profilename, 'profilephonenumber': profilephonenumber, 'profilepic': profilepic})
	except:
		message = None
		detials = None
		return render(request, 'worker/home.html',{'msg': message})


def signup(request):
	message = None
	return render(request, 'worker/signup.html',{'msg':message})


def signupsubmit(request):
	name = request.POST.get('name')
	email = request.POST.get('email')
	password = request.POST.get('password')
	try:
		user = firebaseauth.create_user_with_email_and_password(email, password)
	except Exception as ex:
		message = "Unable to create account. Try again"
		print(ex)
		return render(request, 'worker/home.html',{'msg':message})
	uid = user['localId']
	data = {
		'name':name,
	}
	verfication = {
		'verfication': 'Not verified yet'
	}
	database.child("users").child("worker").child(uid).child('details').set(data)
	count = database.child('users').child('worker').child('workercount').child('count').get().val()
	count = count +1
	database.child('users').child('worker').child(uid).child('details').child('id').set(int(count))
	database.child('users').child('worker').child('workercount').child('count').set(int(count))
	database.child('users').child('worker').child(uid).child('verfication').set(verfication)
	submitdata = {
		'profile': 'No',
		'certificates': 'No',
		'questionnairejava': 'No',
		'questionnairepython': 'No',
		'questionnairemarketing': 'No',
		'questionnairewebdesigner': 'No'
	}
	database.child('users').child('worker').child(uid).child('notifications').child('notificationcount').child('count').set(0)
	database.child('users').child('worker').child(uid).child('Submitted').set(submitdata)
	message = "Your account has created successfully. Now Sign in."
	return render(request, 'worker/signup.html',{'msg':message})


def signin(request):
	details = None
	return render(request, 'worker/signin.html')

def signinsubmit(request):
	email = request.POST.get('email')
	password = request.POST.get('password')
	try:
		user = firebaseauth.sign_in_with_email_and_password(email, password)
	except:
		message = "Invalid Credentials"
		return render(request, 'worker/home.html',{'msg':message})
	session_id = user['idToken']
	request.session['uid'] = str(session_id)
	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	b = a['users'][0]['localId']
	data = database.child('users').child("worker").child(b).child('details').child('name').get().val()
	message = "Your are logged in successfully"
	return render(request, 'worker/home.html',{"details":data,"msg":message})




def logout(request):
	auth.logout(request)
	return redirect(home)



def submitdoc(request):
	return render(request, 'worker/submitdoc.html')

def submitdocsubmit(request):
	url = request.POST.get('url')
	firstname = request.POST.get('firstname')
	lastname = request.POST.get('lastname')	
	phonenumber = request.POST.get('phonenumber')
	description = request.POST.get('description')
	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	a = a['users']
	a = a[0]
	a = a['localId']
	data = {
		'firstname':firstname,
		'lastname': lastname,
		'phonenumber': phonenumber,
		'url':url,
		'description': description,
	}
	abc = database.child('users').child('worker').child(a).child('profile').set(data)
	database.child('users').child('worker').child(a).child('Submitted').child('profile').set('Yes')
	return HttpResponse(abc)



def addcertificates(request):
	return render(request, 'worker/addcertificates.html')


def addcertificatessubmit(request):
	url = request.POST.get('url')
	field = request.POST.get('dropdown')

	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	a = a['users']
	a = a[0]
	a = a['localId']
	certificates = database.child('users').child('worker').child(a).child('certificates').shallow().get().val()
	flag = 0
	if(certificates==None):
		flag=0
	else:
		for i in certificates:
			flag +=1
	name = "certificate" + str(flag)
	data = {
		'field': field,
		'certificate': url,
	}
	numofcertificates = database.child('users').child('worker').child(a).child('certificates').child(field).shallow().get().val()
	mainflag = 0
	if(numofcertificates==None):
		mainflag=0
	else:
		for i in numofcertificates:
			flag +=1
	mainname = "certificate" + str(flag)
	maindata = {
		'url': url,
	}
	database.child('users').child('worker').child(a).child('certificates').child(field).child(mainname).set(maindata)
	database.child('users').child('worker').child(a).child('Submitted').child('certificates').set('Yes')
	return render(request, 'worker/redirect.html')


def editprofile(request): #Have to add another input field for brief introduction of himself
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users']
		a = a[0]
		a = a['localId']
		try:
			editdetails = database.child('users').child("worker").child(a).child('profile').shallow().get().val()
		except:
			return HttpResponse("You haven't submitted your profile yet!")
		firstname = database.child('users').child('worker').child(a).child('profile').child('firstname').get().val()
		lastname = database.child('users').child('worker').child(a).child('profile').child('lastname').get().val()
		phonenumber = database.child('users').child('worker').child(a).child('profile').child('phonenumber').get().val()
		url = database.child('users').child('worker').child(a).child('profile').child('url').get().val()
		name = database.child('users').child('worker').child(a).child('details').child('name').get().val()
		print(name)
		return render(request,'worker/editprofile.html', {'firstname':firstname, 'lastname': lastname,'phonenumber': phonenumber, 'url': url, 'name':name})
	except:
		return render(request, 'worker/editprofile.html')


def editprofilesubmit(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	firstname = request.POST.get('firstname')
	lastname = request.POST.get('lastname')
	phonenumber = request.POST.get('phonenumber')
	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	a = a['users'][0]['localId']
	url = database.child('users').child('worker').child(a).child('profile').child('url').get().val()

	data = {
		'firstname': firstname,
		'lastname': lastname,
		'phonenumber': phonenumber,
		'url': url
	}
	database.child('users').child('worker').child(a).child('profile').set(data)
	return HttpResponse("Profile Updated")


def status(request):	#status should in which company the employee is working currently.
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	certificatesstatus = database.child('users').child('worker').child(a).child('Submitted').child('certificates').get().val()
	profilestatus = database.child('users').child('worker').child(a).child('Submitted').child('profile').get().val()
	questionnairejavastatus = database.child('users').child('worker').child(a).child('Submitted').child('questionnairejava').get().val()
	questionnairepythonstatus = database.child('users').child('worker').child(a).child('Submitted').child('questionnairepython').get().val()
	questionnairemarketingstatus = database.child('users').child('worker').child(a).child('Submitted').child('questionnairemarketing').get().val()
	questionnairewebdesignerstatus = database.child('users').child('worker').child(a).child('Submitted').child('questionnairewebdesigner').get().val()
	status = database.child('users').child('worker').child(a).child('verfication').child('verfication').get().val()
	return render(request, 'worker/status.html', {'status':status, 'certificatesstatus': certificatesstatus,'profilestatus':profilestatus, 'questionnairejavastatus': questionnairejavastatus, 'questionnairepythonstatus': questionnairepythonstatus, 'questionnairemarketingstatus': questionnairemarketingstatus, 'questionnairewebdesignerstatus': questionnairemarketingstatus})


def statussubmit(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	verificationsubmit = request.POST.get('verificationsubmit')
	if verificationsubmit == 'Under Verification':
		database.child('users').child('worker').child(a).child('verfication').child('verfication').set('Under verification')
		return HttpResponse("Your account is submitted for verification")
	return redirect('home')

def questionnaire(request): #We have to make sure that each and every question is required and should implemented with javascript
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in! Go and login to see questionnaire")
	fields = database.child('users').child('worker').child(a).child('certificates').shallow().get().val()
	java = None
	python = None
	marketing = None
	webdesigner = None
	for i in fields:
		if(i=='Java'):
			java = 'yes'
		elif(i=='Python'):
			python = 'yes'
		elif(i=='Marketing'):
			marketing = 'yes'
		elif(i=='WebDesigner'):
			webdesigner = 'yes'
	return render(request, 'worker/questionnaire.html',{'java':java, 'python': python, 'marketing': marketing, 'webdesigner': webdesigner})


def questionnairejava(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in! Go and login to see questionnaire")
	if(database.child('users').child('worker').child(a).child('certificates').child('Java').get().val()):
		javaquestion1 = None
		javaquestion2 = None
		javaquestion3 = None	
		javaquestion1 = database.child('Questionnaire').child('Java').child('Question1').get().val()
		javaquestion2 = database.child('Questionnaire').child('Java').child('Question2').get().val()
		javaquestion3 = database.child('Questionnaire').child('Java').child('Question3').get().val()
		return render(request, 'worker/questionnairejava.html', {'javaquestion1': javaquestion1, 'javaquestion2': javaquestion2,'javaquestion3': javaquestion3})
	elif(database.child('users').child('worker').child(a).child('Submitted').child('questionnairejava').get().val()=='Yes'):
		return HttpResponse("You have submitted your java questionnaire already!")
	else:
		return HttpResponse("You haven't uploaded your java certificates")



def questionnairepython(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in! Go and login to see questionnaire")
	if(database.child('users').child('worker').child(a).child('certificates').child('Python').get().val()):
		pythonquestion1 = None
		pythonquestion2 = None
		pythonquestion3 = None	
		pythonquestion1 = database.child('Questionnaire').child('Python').child('Question1').get().val()
		pythonquestion2 = database.child('Questionnaire').child('Python').child('Question2').get().val()
		pythonquestion3 = database.child('Questionnaire').child('Python').child('Question3').get().val()
		return render(request, 'worker/questionnairepython.html', {'pythonquestion1': pythonquestion1, 'pythonquestion2': pythonquestion2,'pythonquestion3': pythonquestion3})
	elif(database.child('users').child('worker').child(a).child('Submitted').child('questionnairejava').get().val()=='Yes'):
		return HttpResponse("You have submitted your Python questionnaire already!")
	else:
		return HttpResponse("You haven't submitted your python certificates")



def questionnairemarketing(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in! Go and login to see questionnaire")
	if(database.child('users').child('worker').child(a).child('certificates').child('Marketing').get().val()):
		marketingquestion1 = None
		marketingquestion2 = None
		marketingquestion3 = None	
		marketingquestion1 = database.child('Questionnaire').child('Marketing').child('Question1').get().val()
		marketingquestion2 = database.child('Questionnaire').child('Marketing').child('Question2').get().val()
		marketingquestion3 = database.child('Questionnaire').child('Marketing').child('Question3').get().val()
		return render(request, 'worker/questionnairemarketing.html', {'marketingquestion1': marketingquestion1, 'marketingquestion2': marketingquestion2,'marketingquestion3': marketingquestion3})
	elif(database.child('users').child('worker').child(a).child('Submitted').child('Marketing').get().val()=='Yes'):
		return HttpResponse("You have submitted your marketing questionnaire already!")
	else:
		return HttpResponse("You haven't added your marketing certificaters")




def questionnairewebdesigner(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in! Go and login to see questionnaire")
	if(database.child('users').child('worker').child(a).child('certificates').child('WebDesigner').get().val()):
		webdesignerquestion1 = None
		webdesignerquestion2 = None
		webdesignerquestion3 = None	
		webdesignerquestion1 = database.child('Questionnaire').child('WebDesigner').child('Question1').get().val()
		webdesignerquestion2 = database.child('Questionnaire').child('WebDesigner').child('Question2').get().val()
		webdesignerquestion3 = database.child('Questionnaire').child('WebDesigner').child('Question3').get().val()
		return render(request, 'worker/questionnairewebdesigner.html', {'webdesignerquestion1': webdesignerquestion1, 'webdesignerquestion2': webdesignerquestion2,'webdesignerquestion3': webdesignerquestion3})
	elif(database.child('users').child('worker').child(a).child('Submitted').child('questionnairejava').get().val()=='Yes'):
		return HttpResponse("You have submitted your webdesigner already!")
	else:
		return HttpResponse("You haven't added your webdesigner certificates")



def questionnairejavasubmit(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in! Go and login to see questionnaire")
	javaquestion1 = request.POST.get('javaquestion1')
	javaquestion2 = request.POST.get('javaquestion2')
	javaquestion3 = request.POST.get('javaquestion3')
	data = {
		'Question1': javaquestion1,
		'Question2': javaquestion2,
		'Question3': javaquestion3
	}
	database.child('users').child('worker').child(a).child('questionnaire').child('Java').set(data)
	database.child('users').child('worker').child(a).child('Submitted').child('questionnairejava').set('Yes')
	details = database.child('users').child("worker").child(a).child('details').child('name').get().val()
	paneluids = database.child('users').child('panel').get().val()
	paneljavacount = 0
	for i in paneluids:
		if(database.child('users').child('panel').child(i).child('details').child('skill').child('skill').get().val()=='Java'):
			paneljavacount = paneljavacount+1
	workerid = database.child('users').child('worker').child(a).child('details').child('id').get().val()
	result = workerid%paneljavacount
	for i in paneluids:
		if(database.child('users').child('panel').child(i).child('details').child('id').child('id').get().val()==result):
			panelname = database.child('users').child('panel').child(i).child('details').child('email').child('email').get().val()
			database.child('users').child('worker').child(a).child('verifiedby').child('Java').child('email').set(panelname)
			break
	return render(request, 'worker/home.html',{'msg':"Java Questionnaire has submitted successfully", 'details': details})


def questionnairepythonsubmit(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in! Go and login to see questionnaire")
	pythonquestion1 = request.POST.get('pythonquestion1')
	pythonquestion2 = request.POST.get('pythonquestion2')
	pythonquestion3 = request.POST.get('pythonquestion3')
	data = {
		'Question1': pythonquestion1,
		'Question2': pythonquestion2,
		'Question3': pythonquestion3
	}
	database.child('users').child('worker').child(a).child('questionnaire').child('Python').set(data)
	database.child('users').child('worker').child(a).child('Submitted').child('questionnairepython').set('Yes')
	details = database.child('users').child("worker").child(a).child('details').child('name').get().val()
	paneluids = database.child('users').child('panel').get().val()
	panelpythoncount = 0
	for i in paneluids:
		if(database.child('users').child('panel').child(i).child('details').child('skill').child('skill').get().val()=='Python'):
			panelpythoncount = panelpythoncount+1
	workerid = database.child('users').child('worker').child(a).child('details').child('id').get().val()
	result = workerid%panelpythoncount
	for i in paneluids:
		if(str(database.child('users').child('panel').child(i).child('details').child('id').child('id').get().val())==str(result) and str(database.child('users').child('panel').child(i).child('details').child('skill').child('skill').get().val())=='Python'):
			panelname = database.child('users').child('panel').child(i).child('details').child('email').child('email').get().val()
			database.child('users').child('worker').child(a).child('verifiedby').child('Python').child('email').set(panelname)
	return render(request, 'worker/home.html',{'msg':"Python Questionnaire has submitted successfully", 'details': details})

def questionnairemarketingsubmit(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in! Go and login to see questionnaire")
	marketingquestion1 = request.POST.get('marketingquestion1')
	marketingquestion2 = request.POST.get('marketingquestion2')
	marketingquestion3 = request.POST.get('marketingquestion3')
	data = {
		'Question1': marketingquestion1,
		'Question2': marketingquestion2,
		'Question3': marketingquestion3
	}
	database.child('users').child('worker').child(a).child('questionnaire').child('Marketing').set(data)
	database.child('users').child('worker').child(a).child('Submitted').child('questionnairemarketing').set('Yes')
	details = database.child('users').child("worker").child(a).child('details').child('name').get().val()
	paneluids = database.child('users').child('panel').get().val()
	panelmarketingcount = 0
	for i in paneluids:
		if(database.child('users').child('panel').child(i).child('details').child('skill').child('skill').get().val()=='Marketing'):
			panelmarketingcount = panelmarketingcount+1
	workerid = database.child('users').child('worker').child(a).child('details').child('id').get().val()
	result = workerid%panelmarketingcount
	for i in paneluids:
		if(database.child('users').child('panel').child(i).child('details').child('id').child('id').get().val()==result):
			panelname = database.child('users').child('panel').child(i).child('details').child('email').child('email').get().val()
			database.child('users').child('worker').child(a).child('verifiedby').child('Marketing').child('email').set(panelname)
			break
	return render(request, 'worker/home.html',{'msg':"Marketing Questionnaire has submitted successfully", 'details': details})




def questionnairewebdesignersubmit(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in! Go and login to see questionnaire")
	webdesignerquestion1 = request.POST.get('webdesignerquestion1')
	webdesignerquestion2 = request.POST.get('webdesignerquestion2')
	webdesignerquestion3 = request.POST.get('webdesignerquestion3')
	data = {
		'Question1': webdesignerquestion1,
		'Question2': webdesignerquestion2,
		'Question3': webdesignerquestion3
	}
	database.child('users').child('worker').child(a).child('questionnaire').child('WebDesigner').set(data)
	database.child('users').child('worker').child(a).child('Submitted').child('questionnairewebdesigner').set('Yes')
	details = database.child('users').child("worker").child(a).child('details').child('name').get().val()
	paneluids = database.child('users').child('panel').get().val()
	panelwebdesignercount = 0
	for i in paneluids:
		if(database.child('users').child('panel').child(i).child('details').child('skill').child('skill').get().val()=='WebDesigner'):
			panelwebdesignercount = panelwebdesignercount+1
	workerid = database.child('users').child('worker').child(a).child('details').child('id').get().val()
	result = workerid%panelwebdesignercount
	for i in paneluids:
		if(database.child('users').child('panel').child(i).child('details').child('id').child('id').get().val()==result):
			panelname = database.child('users').child('panel').child(i).child('details').child('email').child('email').get().val()
			database.child('users').child('worker').child(a).child('verifiedby').child('WebDesigner').child('email').set(panelname)
			break
	return render(request, 'worker/home.html',{'msg':"Webdeisgning Questionnaire has submitted successfully", 'details': details})


def agreement(request, companyuid, notificationcount):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	companyuids = database.child('users').child('Company').get().val()
	if(companyuid in companyuids):
		companyname = database.child('users').child('Company').child(companyuid).child('profile').child('companyname').get().val()
		skill = database.child('users').child('worker').child(a).child('notifications').child(notificationcount).child('skill').get().val()
		time = database.child('users').child('worker').child(a).child('notifications').child(notificationcount).child('time').get().val()
		return render(request, 'worker/agreement.html',{'companyname':companyname,'skill':skill, 'time':time})
	else:
		return HttpResponse("NO data found with that url")
		#After this agreement should be saved(proceed/decline)



def count(request):
	data = database.child('users').child('worker').shallow().get().val()
	return HttpResponse(data)
	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	a = a['users']
	a = a[0]
	a = a['localId']

	certificates = database.child('users').child('worker').child(a).child('certificates').shallow().get().val()
	flag =0
	for i in certificates:
		flag+=1
	return HttpResponse(flag)




def seeresults(request):
	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	a = a['users'][0]['localId']
	if(database.child('users').child('worker').child(a).child('profile').get().val()!=None):
		return HttpResponse("None")
	return HttpResponse("something")




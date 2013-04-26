# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to 
from client.models import *
import hashlib
import simplejson as json
from django.http import HttpResponseRedirect
import const
from django.core.mail import send_mail

# main page
@render_to('main/index.html')
def home(request):
	return {'request': request}

# sign in client
def login(request):
	result = 'error'
	password = hashlib.md5()
	password.update(request.GET['password'])
	client = Client.objects.filter(email=request.GET['email'], password=password.hexdigest())	
	try: 
		if client[0].email!='' and len(client)==1:
			request.session['username'] = client[0].email
			result = 'ok'
	except:
		result = 'error'
	return HttpResponse( json.dumps({'result':result}), mimetype="application/json" )

# sign up client
def register(request):
	password = hashlib.md5()
	password.update(request.GET['password'])
	ticket = hashlib.md5()
	ticket.update(request.GET['password']+request.GET['email'])
	client = Client(email=request.GET['email'], password=password.hexdigest(), ticket= ticket.hexdigest())
	client.save()
	request.session['username'] = client.email
	send_mail(const.REGISTER_THEMA_EMAIL, const.REGISTER_TEXT_EMAIL, const.EMAIL_FROM, [client.email], fail_silently=False)
	return HttpResponse( json.dumps({'result':'ok', 'username':client.email}), mimetype="application/json" )

# forget password
@render_to('main/forget.html')
def forget(request):
	return {'request': request}

# logout for profile
def logout(request):
	request.session['username']=''
	return HttpResponseRedirect("/")
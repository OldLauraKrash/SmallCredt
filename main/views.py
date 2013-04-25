# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to 
from client.models import *
import hashlib
import simplejson as json
from django.http import HttpResponseRedirect
from django.db.models import Q

@render_to('main/index.html')
def home(request):
	return {'request': request}

def login(request):
	result = 'error'
	hsh = hashlib.md5()
	hsh.update(request.GET['password'])
	client = Client.objects.get(email__exact=request.GET['email'], password__exact=hsh.hexdigest())
	try: 
		if client.email!='':
			request.session['username'] = client.email
			result = 'ok'
	except:
		result = 'error'
	return HttpResponse( json.dumps({'result':result}), mimetype="application/json" )

def register(request):
	hsh = hashlib.md5()
	hsh.update(request.GET['password'])
	client = Client(email=request.GET['email'], password=hsh.hexdigest())
	client.save()
	request.session['username'] = client.email
	return HttpResponse( json.dumps({'result':'ok', 'username':client.email}), mimetype="application/json" )

def logout(request):
	request.session['username']=''
	return HttpResponseRedirect("/")
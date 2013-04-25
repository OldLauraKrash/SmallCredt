# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to 
from client.models import *
import hashlib
import simplejson as json
from django.http import HttpResponseRedirect

@render_to('main/index.html')
def home(request):
	return {'request': request}

def login(request):
	result = 'error'
	hsh = hashlib.md5()
	hsh.update(request.GET['password'])
	client = Client.objects.filter(email=request.GET['email'], password=hsh.hexdigest())	
	try: 
		if client[0].email!='' and len(client)==1:
			request.session['username'] = client[0].email
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
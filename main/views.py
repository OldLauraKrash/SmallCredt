# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to 
from client.models import *
import hashlib
import simplejson as json

@render_to('main/index.html')
def home(request):
	return {}

def login(request):
	return {}

def register(request):
	hsh = hashlib.md5()
	hsh.update(request.GET['password'])
	client = Client(email=request.GET['email'], password=hsh.hexdigest())
	client.save()
	request.session['username'] = client.email
	return HttpResponse( json.dumps({'result':'ok', 'username':client.email}), mimetype="application/json" )

def logout(request):
	return {}
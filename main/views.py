# -*- coding: utf-8 -*
from annoying.decorators import render_to 
#from client.models import *
import simplejson as json

@render_to('main/index.html')
def home(request):
	return {}

def login(request):
	return {}

def register(request):
	return HttpResponse( json.dumps({'result':request.POST}), mimetype="application/json" )
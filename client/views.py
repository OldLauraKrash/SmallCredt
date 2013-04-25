# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to 
from client.models import *
import hashlib
import simplejson as json
from client.models import *

@render_to('profile/apply.html')
def profile(request):
	client = Client.objects.get(email=request.session['username'] )
	return {'request': request, 'client': client}

@render_to('profile/credit-offers.html')
def credit_offers(request):
	return {'request': request}	

@render_to('profile/account.html')
def account(request):
	return {'request': request}	

@render_to('profile/statements.html')
def statements(request):
	return {'request': request}	
	

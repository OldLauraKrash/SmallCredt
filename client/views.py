# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to 
from client.models import *
import hashlib
import simplejson as json
from client.models import *
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

# check auth client
def check_auth(request):
	try: 
		if request.session['username']=='':
			return True
		else:
			return False
	except:
		return True	

# auth on page for profile
@render_to('profile/auth.html')
def auth(request):
	return {'request': request}

# profile client
@render_to('profile/apply.html')
def profile(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")

	client = Client.objects.get(email=request.session['username'])
	return {'request': request, 'client': client}

# credit offers for profile
@render_to('profile/credit-offers.html')
def credit_offers(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")

	return {'request': request}	

# account for profile
@render_to('profile/account.html')
def account(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")

	return {'request': request}	

# statements for profile
@render_to('profile/statements.html')
def statements(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")

	return {'request': request}
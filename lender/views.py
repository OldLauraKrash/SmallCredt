# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to 
from client.models import *
import hashlib
import simplejson as json
from lender.models import *
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# profile lender
@render_to('lender/account.html')
def lender_account(request):
	system_account = System_account.objects.get(email=request.session['username'])
	try: 
		lender = Lender.objects.get(system_account=system_account.id)
	except:
		lender = ''
	return {'request': request, 'lender':lender, 'system_account':system_account}

# statements lender
@render_to('lender/statements.html')
def lender_statements(request):
	return {'request': request}

# portfolio lender
@render_to('lender/portfolio.html')
def lender_portfolio(request):
	return {'request': request}

# edit lender
@render_to('lender/edit.html')
def lender_edit(request):
	system_account = System_account.objects.get(email=request.session['username'])
	try: 
		lender = Lender.objects.get(system_account=system_account.id)
	except:
		lender = ''
	return {'request': request, 'lender':lender}

# marketplace lender
@render_to('lender/marketplace.html')
def lender_marketplace(request):
	return {'request': request}

# save data lender
def save_lender(request):
	system_account = System_account.objects.get(email=request.session['username'])
	try: 
		lender = Lender.objects.get(system_account=system_account.id)
	except:
		lender = Lender()
		lender.system_account=system_account	
		lender.save()
	lender = Lender.objects.get(system_account=system_account.id)
	lender.suffix = request.GET['suffix']
	lender.first_name = request.GET['first']
	lender.middle_name = request.GET['middle']
	lender.last_name = request.GET['last']
	lender.home_phone = request.GET['home_phone']
	lender.cell_phone = request.GET['cell_phone']
	lender.title = request.GET['title']
	lender.company = request.GET['company']
	lender.street = request.GET['street']
	lender.city = request.GET['city']
	lender.zip_code = request.GET['zip_code']
	try: 
		state=State.objects.get(name=request.GET['state'])
		lender.state=state
	except:
		lender.state = ''
	try: 
		country=Country.objects.get(name=request.GET['country'])
		lender.country=country
	except:
		lender.country = ''
	try: 
		geography=Geography.objects.get(name=request.GET['geography'])
		lender.geography=geography
	except:
		lender.geography = ''
	try: 
		risk_level=Risk_level.objects.get(name=request.GET['risk_level'])
		lender.risk_level=risk_level
	except:
		lender.risk_level = ''
	try: 
		industry=Industry.objects.get(name=request.GET['industry'])
		lender.industry=industry
	except:
		lender.industry = ''		
	lender.save()	
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# get geography
def get_geography(request):
	result = Geography.objects.all()
	categories = []
	for category in result:
		categories.append(category.name)	
	return HttpResponse( json.dumps({'categories':categories}), mimetype="application/json" )

# get risk level
def get_risk_level(request):
	result = Risk_level.objects.all()
	categories = []
	for category in result:
		categories.append(category.name)	
	return HttpResponse( json.dumps({'categories':categories}), mimetype="application/json" )
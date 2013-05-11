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
	return {'request': request}

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
	lender.save()	
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )
# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to 
from client.models import *
import hashlib
import simplejson as json
from lender.models import *
from loan.models import *
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# check auth client
def check_auth(request):
	try: 
		if request.session['username']=='':
			return True
		else:
			return False
	except:
		return True	

# profile lender
@render_to('lender/account.html')
def lender_account(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
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
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	system_account = System_account.objects.get(email=request.session['username'])
	try: 
		lender = Lender.objects.get(system_account=system_account.id)
		lists = Loan_offer.objects.filter(lender=lender, enable=True)
	except:
		lists = ''
	return {'request': request, 'lists':lists}

# edit lender
@render_to('lender/edit.html')
def lender_edit(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	system_account = System_account.objects.get(email=request.session['username'])
	try: 
		lender = Lender.objects.get(system_account=system_account.id)
	except:
		lender = ''
	return {'request': request, 'lender':lender}

# marketplace lender
@render_to('lender/marketplace.html')
def lender_marketplace(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")	
	borrowers = Borrower.objects.filter(accepted = True)
	lists = []
	for borrower in borrowers:
		system_account = System_account.objects.get(email=borrower.system_account)
		business = Business.objects.get(system_account=borrower.system_account)
		business_measure = Business_measure.objects.get(system_account=borrower.system_account)
		locale = str(business.city)+', '+str(business.state)
		risk = borrower.risk_level
		lists.append(dict([('date', borrower.created),
							('id', system_account.id), 
							('amount', business_measure.amount),
							('industry', business.industry),
							('locale', locale),
							('risk', risk),
							('name', business.business_name)]))

	return {'request': request, 'lists':lists}

# bid
def bid(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	system_account = System_account.objects.get(email=request.session['username'])
	lender = Lender.objects.get(system_account=system_account.id)

	system_account = System_account.objects.get(id=request.GET['id'])
	borrower = Borrower.objects.get(system_account=system_account)
	borrower.created = datetime.now()
	borrower.save()

	loan_offer = Loan_offer()
	loan_offer.lender = lender
	loan_offer.borrower = borrower
	loan_offer.amount = request.GET['amount']
	loan_offer_daily_repayment_sale = request.GET['daily']
	loan_offer.discount = request.GET['discount']
	loan_offer.enable = True
	loan_offer.status = 1
	loan_offer.save() 

	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

#lender info
@render_to('lender/info.html') 
def info(request, id):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	try: 
		lender = Lender.objects.get(id=id)
	except:
		lender = ''
	return {'request': request, 'lender':lender, 'email':lender.system_account.email}


# decline
def decline(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	system_account = System_account.objects.get(email=request.session['username'])
	lender = Lender.objects.get(system_account=system_account.id)

	system_account = System_account.objects.get(id=request.GET['id'])
	borrower = Borrower.objects.get(system_account=system_account)

	loan_offer = Loan_offer()
	loan_offer.lender = lender
	loan_offer.borrower = borrower
	loan_offer.enable = False
	loan_offer.status = 2
	loan_offer.save() 	
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# marketplace lender
@render_to('lender/marketplace_borrower.html')
def lender_marketplace_borrower(request, id):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	system_account = System_account.objects.get(email=request.session['username'])
	try:
		lender = Lender.objects.get(system_account=system_account)
	except:
		lender = ''

	system_account = System_account.objects.get(id=id)
	borrower = Borrower.objects.get(system_account=system_account)

	try:
		loan_offer = Loan_offer.objects.get(lender=lender, borrower=borrower, enable = True)
	except:
		loan_offer = ''

	system_account = System_account.objects.get(id=id)
	business = Business.objects.get(system_account=system_account)
	borrower = Borrower.objects.get(system_account=system_account)
	bank_file = Bank_file.objects.filter(system_account=system_account.id)
	processor_file = Processor_file.objects.filter(system_account=system_account.id)
	financial_file =  Financial_file.objects.filter(system_account=system_account.id)
	business_measure = Business_measure.objects.get(system_account=borrower.system_account)
	return {'request': request, 'bank_file':bank_file, 'financial_file':financial_file, 'processor_file':processor_file, 'loan_offer':loan_offer, 'business': business, 'system_account': system_account, 'borrower': borrower, 'business_measure':business_measure}

# save data lender
def save_lender(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
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
		risk=Risk.objects.get(name=request.GET['risk'])
		lender.risk=risk
	except:
		lender.risk = ''
	try: 
		industry=Industry.objects.get(name=request.GET['industry'])
		lender.industry=industry
	except:
		lender.industry = ''		
	lender.save()	
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# get geography
def get_geography(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	result = Geography.objects.all()
	categories = []
	for category in result:
		categories.append(category.name)	
	return HttpResponse( json.dumps({'categories':categories}), mimetype="application/json" )

# get risk level
def get_risk_lender(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	result = Risk.objects.all()
	categories = []
	for category in result:
		categories.append(category.name)	
	return HttpResponse( json.dumps({'categories':categories}), mimetype="application/json" )
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
	system_account = System_account.objects.get(email=request.session['username'])
	try: 
		lender = Lender.objects.get(system_account=system_account.id)
		lists = Loan_offer.objects.filter(lender=lender)
	except:
		lists = ''
	return {'request': request, 'lists':lists}

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
	borrowers = Borrower.objects.filter(borrower_status = True)
	lists = []
	for borrower in borrowers:
		system_account = System_account.objects.get(email=borrower.system_account)
		business = Business.objects.get(system_account=borrower.system_account)
		business_measure = Business_measure.objects.get(system_account=borrower.system_account)
		locale = str(business.city)+', '+str(business.state)
		lists.append(dict([('date', borrower.created),
							('id', system_account.id), 
							('amount', business_measure.amount),
							('industry', business.industry),
							('locale', locale),
							('name', business.business_name)]))

	return {'request': request, 'lists':lists}

# bid
def bid(request):
	loan_offer = Loan_offer()
	system_account = System_account.objects.get(email=request.session['username'])
	lender = Lender.objects.get(system_account=system_account.id)

	system_account = System_account.objects.get(id=request.GET['id'])
	borrower = Borrower.objects.get(system_account=system_account)

	loan_offer = Loan_offer()
	loan_offer.lender = lender
	loan_offer.borrower = borrower
	loan_offer.amount = request.GET['amount']
	loan_offer_daily_repayment_sale = request.GET['daily']
	loan_offer.discount = request.GET['discount']
	loan_offer.status = 1
	loan_offer.save() 	
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# decline
def decline(request):
	loan_offer = Loan_offer()
	system_account = System_account.objects.get(email=request.session['username'])
	lender = Lender.objects.get(system_account=system_account.id)

	system_account = System_account.objects.get(id=request.GET['id'])
	borrower = Borrower.objects.get(system_account=system_account)

	loan_offer = Loan_offer()
	loan_offer.lender = lender
	loan_offer.borrower = borrower
	loan_offer.status = 2
	loan_offer.save() 	
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# marketplace lender
@render_to('lender/marketplace_borrower.html')
def lender_marketplace_borrower(request, id):
	system_account = System_account.objects.get(email=request.session['username'])
	lender = Lender.objects.get(system_account=system_account.id)

	system_account = System_account.objects.get(id=id)
	borrower = Borrower.objects.get(system_account=system_account)

	try:
		loan_offer = Loan_offer.objects.get(lender=lender, borrower=borrower)
		loan_offer = False
	except:
		loan_offer = True

	system_account = System_account.objects.get(id=id)
	business = Business.objects.get(system_account=system_account)
	borrower = Borrower.objects.get(system_account=system_account)
	business_measure = Business_measure.objects.get(system_account=borrower.system_account)
	return {'request': request, 'loan_offer':loan_offer, 'business': business, 'system_account': system_account, 'borrower': borrower, 'business_measure':business_measure}

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
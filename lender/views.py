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
import const
import sys

# check auth client
def check_auth(request):
  	"""
    Checking auth the user
    """
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
	'''
	Information lender account

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account` and :model:`lender.Lender`

	**Template:**

	:template:`lender/account.html`
	'''
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	system_account = System_account.objects.get(email=request.session['username'])
	try: 
		lender = Lender.objects.get(system_account=system_account.id)
	except:
		lender = ''
	risk_tags = Risk_tag.objects.filter(system_account=system_account)
	geography_tags = Geography_tag.objects.filter(system_account=system_account.id)
	industry_tags = Industry_tag.objects.filter(system_account=system_account)	
	return {'request': request, 'lender':lender, 'risk_tags':risk_tags, 'geography_tags':geography_tags, 'industry_tags':industry_tags, 'system_account':system_account}

# statements lender
@render_to('lender/statements.html')
def lender_statements(request):
	'''
	Lender statements

	**Context**

	``request``

	**Template:**

	:template:`lender/statements.html`
	'''
	return {'request': request}

# status show lender
def status_show_lender(x):
    return {
        None: 'Outstanding',
        1: 'Accepted',
        2: 'Declined'
    }[x]

# portfolio lender
@render_to('lender/portfolio.html')
def lender_portfolio(request):
	'''
	Lender portfilio page

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`, :model:`lender.Lender`, :model:`loan.Loan_offer`
	    and :model:`client.Business`

	**Template:**

	:template:`lender/portfolio.html`
	'''
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	system_account = System_account.objects.get(email=request.session['username'])
	try: 
		lender = Lender.objects.get(system_account=system_account.id)
		result = Loan_offer.objects.filter(lender=lender, enable=True)
		lists = []

		for value in result:
			status = status_show_lender(value.status_lender)
			business = Business.objects.get(system_account=value.borrower.system_account)
			lists.append(dict([('offer_date', value.offer_date),
				('id', value.borrower.system_account.id), 
				('borrower', business.business_name),
				('amount', value.amount),
				('discount', value.discount),
				('daily_repayment_sale', value.daily_repayment_sale),
				('status', status)]))
	except:
		lists = ''
	return {'request': request, 'lists':lists}

# edit lender
@render_to('lender/edit.html')
def lender_edit(request):
	'''
	Lender edit page

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`, :model:`lender.Lender`

	**Template:**

	:template:`lender/edit.html`
	'''
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	system_account = System_account.objects.get(email=request.session['username'])
	try: 
		lender = Lender.objects.get(system_account=system_account.id)
	except:
		lender = ''

	risk_tags = Risk_tag.objects.filter(system_account=system_account)
	geography_tags = Geography_tag.objects.filter(system_account=system_account.id)
	industry_tags = Industry_tag.objects.filter(system_account=system_account)	
	return {'request': request, 'lender':lender, 'risk_tags': risk_tags, 'industry_tags': industry_tags, 'geography_tags': geography_tags}

# marketplace lender
@render_to('lender/marketplace.html')
def lender_marketplace(request):
	'''
	Lender marketplace page

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`, :model:`client.Borrower`, :model:`client.Business`, :model:`client.Business_measure`

	**Template:**

	:template:`lender/marketplace.html`
	'''
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
	'''
	Accepting the offer

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`, :model:`client.Business_measure`, :model:`lender.Lender`
	    and :model:`loan.Loan_offer` 
	'''
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	system_account = System_account.objects.get(email=request.session['username'])
	lender = Lender.objects.get(system_account=system_account.id)

	system_account = System_account.objects.get(id=request.GET['id'])
	borrower = Borrower.objects.get(system_account=system_account)
	business_measure = Business_measure.objects.get(system_account=system_account)
	borrower.created = datetime.now()
	borrower.save()

	loan_offer = Loan_offer()
	loan_offer.lender = lender
	loan_offer.borrower = borrower
	loan_offer.amount = request.GET['amount']
	loan_offer.daily_repayment_sale = request.GET['daily']
	loan_offer.discount = request.GET['discount']
	loan_offer.repaid_amount = int(request.GET['amount'])*float(request.GET['discount'])
	total = round(int(request.GET['amount'])*float(request.GET['discount'])) / round(int(business_measure.monthly_sales) * int(request.GET['daily'])/100)
	loan_offer.estimated_repaid_term = int(total)
	loan_offer.enable = True
	loan_offer.status = 1
	loan_offer.save() 

	if settings.PROD:
		send_mail(const.LOAN_THEMA, const.LOAN_TEXT, const.EMAIL_FROM, [loan_offer.borrower.system_account.email], fail_silently=False)	

	return HttpResponse( json.dumps({'result':'ok', 'id':loan_offer.id}), mimetype="application/json" )

#lender info
@render_to('lender/info.html') 
def info(request, id):
	'''
	Information about lender page

	**Context**

	``request``

	``models``

	    An instance of :model:`lender.Lender`

	**Template:**

	:template:`lender/info.html`
	'''	
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	try: 
		lender = Lender.objects.get(id=id)
	except:
		lender = ''
	return {'request': request, 'lender':lender, 'email':lender.system_account.email}


# decline
def decline(request):
	'''
	Declining the offer

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`, `lender.Lender`, `client.Business_measure`, `lender.Lender`
	    and `loan.Loan_offer` 
	'''
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
	loan_offer.daily_repayment_sale = 0
	loan_offer.discount = 0
	loan_offer.status = 2
	loan_offer.save()
	 	
	return HttpResponse( json.dumps({'result':'ok', 'id':loan_offer.id}), mimetype="application/json" )

# marketplace lender
@render_to('lender/marketplace_borrower.html')
def lender_marketplace_borrower(request, id):
	'''
	Lender marketplace borrower page

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`, :model:`client.Borrower`, :model:`client.Business`, :model:`client.Business_measure`,
	    :model:`client.Processor_file`, :model:`client.Financial_file`, :model:`client.Financial_file`

	**Template:**

	:template:`lender/marketplace_borrower.html`
	'''
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

# save tags
def save_lender_tag(request):
	'''
	Save lender lists

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`, :model:`lender.GeographyList`, :model:`lender.RiskList`, :model:`client.IndustryList`
	'''
	if request.GET['type']=='risk':
		system_account = System_account.objects.get(email=request.session['username'])
		risk = Risk_tag()
		risk.system_account = system_account
		risk.name = request.GET['name']
		risk.save()

	if request.GET['type']=='geography':
		system_account = System_account.objects.get(email=request.session['username'])
		geography = Geography_tag()
		geography.system_account = system_account
		geography.name = request.GET['name']
		geography.save()

	if request.GET['type']=='industry':
		system_account = System_account.objects.get(email=request.session['username'])
		industry = Industry_tag()
		industry.system_account = system_account
		industry.name = request.GET['name']
		industry.save()

	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# remove item in tags
def remove_item_tag(request):
	'''
	Remove item in list

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`, :model:`lender.GeographyList`, :model:`lender.RiskList`, :model:`client.IndustryList`
	'''
	try: 
		if request.GET['type']=='risk':
			risk_tag = Risk_tag.objects.get(pk=request.GET['id'])
			if str(risk_tag.system_account) == request.session['username']:
				risk_tag.delete()
	except:
		risk_tag = ''

	try: 
		if request.GET['type']=='industry':
			industry_tag = Industry_tag.objects.get(pk=request.GET['id'])
			if str(industry_tag.system_account) == request.session['username']:
				industry_tag.delete()
	except:
		industry_tag = ''

	try:		
		if request.GET['type']=='geography':
			geography_tag = Geography_tag.objects.get(pk=request.GET['id'])
			if str(geography_tag.system_account) == request.session['username']:
				geography_tag.delete()
	except:
		geography_tag = ''
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# save data lender
def save_lender(request):
	'''
	Save lender's information

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`, :model:`lender.Lender`, :model:`client.State`, :model:`client.Country`,
	    :model:`client.Industry`, :model:`lender.Geography` and :model:`lender.Risk`
	'''
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
	"""
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
	"""		
	lender.save()	
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# get geography
def get_geography(request):
	'''
	Get geography list

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`, :model:`lender.Geography`
	'''
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	result = Geography.objects.all()
	categories = []
	for category in result:
		categories.append(category.name)	
	return HttpResponse( json.dumps({'categories':categories}), mimetype="application/json" )

# get risk level
def get_risk_lender(request):
	'''
	Get risk list

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`, :model:`lender.Risk`
	'''
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	result = Risk.objects.all()
	categories = []
	for category in result:
		categories.append(category.name)	
	return HttpResponse( json.dumps({'categories':categories}), mimetype="application/json" )
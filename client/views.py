# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to 
from client.models import *
import hashlib
import simplejson as json
from client.models import *
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings

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
	business = Business.objects.get(client=client.id)
	loan_offer = Loan_offer.objects.get(client=client.id)
	try:
		loan_offer.amount = request.GET['amount'] + "000"
		loan_offer.save()
	except:
		loan_offer = Loan_offer.objects.get(client=client.id)
	return {'request': request, 'client': client, 'business':business, 'loan_offer':loan_offer}

# qualify
@render_to('profile/qualify.html')
def qualify(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	client = Client.objects.get(email=request.session['username'])
	loan_offer = Loan_offer.objects.get(client=client.id)
	return {'request': request, 'loan_offer':loan_offer}

# accepted
@render_to('profile/accepted.html')
def accepted(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	client = Client.objects.get(email=request.session['username'])
	bank = Bank.objects.get(client=client.id)
	return {'request': request, 'bank': bank}

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
	client = Client.objects.get(email=request.session['username'])
	business = Business.objects.get(client=client.id)
	loan_offer = Loan_offer.objects.get(client=client.id)
	bank = Bank.objects.get(client=client.id)
	return {'request': request, 'client': client, 'business':business, 'loan_offer':loan_offer, 'bank': bank}

# statements for profile
@render_to('profile/statements.html')
def statements(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	return {'request': request}

# save data for profile page
def save_profile_main(request):
	client = Client.objects.get(email=request.session['username'])
	client.suffix = request.GET['suffix']
	client.first_name = request.GET['first_name']
	client.middle_name = request.GET['middle_name']
	client.last_name = request.GET['last_name']
	client.other_name = request.GET['other_name']
	client.street = request.GET['street']
	client.city = request.GET['city']
	try: 
		state=State.objects.get(name=request.GET['state'])
		client.state=state
	except:
		client.state = ''
	client.zip_code = request.GET['zip_code']
	try: 
		country=Country.objects.get(name=request.GET['country'])
		client.country=country
	except:
		client.country = ''	
	client.home_phone = request.GET['home_phone']
	client.cell_phone = request.GET['cell_phone']
	client.date_of_birth = request.GET['date_of_birth']
	client.save()
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# save data for profile business page
def save_profile_business(request):
	client = Client.objects.get(email=request.session['username'])
	business = Business.objects.get(client=client.id)
	business.business_name = request.GET['business_name']
	business.dba = request.GET['dba']
	try: 
		legal=Legal.objects.get(name=request.GET['legal_form'])
		business.legal_form=legal
	except:
		business.legal_form = ''
	try: 
		state_of_incorporation=State.objects.get(name=request.GET['state_of_incorporation'])
		business.state_of_incorporation=state_of_incorporation
	except:
		business.state_of_incorporation = ''

	business.date_founded = request.GET['date_founded']
	business.street = request.GET['street']
	business.city = request.GET['city']
	try: 
		state=State.objects.get(name=request.GET['state'])
		business.state=state
	except:
		business.state = ''
	business.zip_code = request.GET['zip_code']
	try: 
		country=Country.objects.get(name=request.GET['country'])
		business.country=country
	except:
		business.country = ''
	business.business_phone = request.GET['business_phone']
	try: 
		industry=Industry.objects.get(name=request.GET['industry'])
		business.industry=industry
	except:
		business.industry = ''
	business.save()
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# save data for profile credit page
def save_profile_credit(request):
	client = Client.objects.get(email=request.session['username'])
	loan_offer = Loan_offer.objects.get(client=client.id)
	loan_offer.amount = request.GET['amount']
	loan_offer.monthly_sales = request.GET['monthly_sales']
	loan_offer.revenue = request.GET['revenue']
	loan_offer.net_profit = request.GET['profit']
	loan_offer.save()
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# save data for profile bank
def save_profile_bank(request):
	client = Client.objects.get(email=request.session['username'])
	bank = Bank.objects.get(client=client.id)
	bank.ein = request.GET['ein']
	bank.social_security_number = request.GET['social_security_number']
	#bank.bank_name = request.GET['bank_name']
	#bank.bank_username = request.GET['bank_username']
	#bank.bank_password = request.GET['bank_password']
	bank.save()
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# get legal legal_form
def get_legal_form(request):
	result = Legal.objects.all()
	categories = []
	for category in result:
		categories.append(category.name)	
	return HttpResponse( json.dumps({'categories':categories}), mimetype="application/json" )	

# get state
def get_state(request):
	result = State.objects.all()
	categories = []
	for category in result:
		categories.append(category.name)	
	return HttpResponse( json.dumps({'categories':categories}), mimetype="application/json" )	

# get country
def get_country(request):
	result = Country.objects.all()
	categories = []
	for category in result:
		categories.append(category.name)	
	return HttpResponse( json.dumps({'categories':categories}), mimetype="application/json" )

# get industry
def get_industry(request):
	result = Industry.objects.all()
	categories = []
	for category in result:
		categories.append(category.name)	
	return HttpResponse( json.dumps({'categories':categories}), mimetype="application/json" )
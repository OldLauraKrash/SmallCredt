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
	return {'request': request, 'client': client, 'business':business, 'loan_offer':loan_offer}

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
	return {'request': request, 'client': client, 'business':business, 'loan_offer':loan_offer}

# statements for profile
@render_to('profile/statements.html')
def statements(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	return {'request': request}

# save data for profile page
def save_profile_main(request):
	client = Client.objects.get(email=request.session['username'])
	client.suffix = request.GET['general-form-profile-your-name-first']
	client.first_name = request.GET['general-form-profile-your-name-second']
	client.middle_name = request.GET['general-form-profile-your-name-third']
	client.last_name = request.GET['general-form-profile-your-name-four']
	client.other_name = request.GET['general-form-profile-your-name-five']
	client.street = request.GET['general-form-profile-address-first']
	client.city = request.GET['general-form-profile-address-second']
	client.state = request.GET['general-form-profile-address-third']
	client.zip_code = request.GET['general-form-profile-address-four']
	client.country = request.GET['general-form-profile-address-five']	
	client.home_phone = request.GET['general-form-profile-phone']
	client.cell_phone = request.GET['general-form-profile-phone-second']
	client.date_of_birth = request.GET['general-form-profile-date']
	client.save()
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# save data for profile business page
def save_profile_business(request):
	client = Client.objects.get(email=request.session['username'])
	business = Business.objects.get(client=client.id)
	business.business_name = request.GET['general-form-profile-business-name-first']
	business.dba = request.GET['general-form-profile-business-name-second']
	business.legal_form = request.GET['general-form-profile-business-legal-first']
	business.state_of_incorporation = request.GET['general-form-profile-business-legal-second']
	business.date_founded = request.GET['general-form-profile-business-legal-third']
	business.street = request.GET['general-form-profile-business-address-first']
	business.city = request.GET['general-form-profile-business-address-second']
	business.state = request.GET['general-form-profile-business-address-third']
	business.zip_code = request.GET['general-form-profile-business-address-four']
	business.country = request.GET['general-form-profile-business-address-country']
	business.business_phone = request.GET['business-phone']
	business.industry = request.GET['industry']
	business.save()
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# save data for profile credit page
def save_profile_credit(request):
	client = Client.objects.get(email=request.session['username'])
	loan_offer = Loan_offer.objects.get(client=client.id)
	loan_offer.amount = request.GET['loan-amount']
	loan_offer.monthly_sales = request.GET['monthly-sales']
	loan_offer.revenue = request.GET['revenue']
	loan_offer.net_profit = request.GET['profit']
	loan_offer.save()
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )
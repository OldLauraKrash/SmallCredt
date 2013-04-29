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
	client.suffix = request.GET['suffix']
	client.first_name = request.GET['first_name']
	client.middle_name = request.GET['middle_name']
	client.last_name = request.GET['last_name']
	client.other_name = request.GET['other_name']
	client.street = request.GET['street']
	client.city = request.GET['city']
	#client.state = request.GET['state']
	client.zip_code = request.GET['zip_code']
	#client.country = request.GET['country']	
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
	#business.legal_form = request.GET['legal_form']
	business.state_of_incorporation = request.GET['state_of_incorporation']
	business.date_founded = request.GET['date_founded']
	business.street = request.GET['street']
	business.city = request.GET['city']
	#business.state = request.GET['state']
	business.zip_code = request.GET['zip_code']
	#business.country = request.GET['country']
	business.business_phone = request.GET['business_phone']
	#business.industry = request.GET['industry']
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
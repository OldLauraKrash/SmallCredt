# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to 
from client.models import *
import hashlib
import simplejson as json
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from loan.models import *
import const
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# check auth client
def check_auth(request):
	try: 
		if request.session['username']=='':
			return 0
		else:
			system_account = System_account.objects.get(email=request.session['username'])
			if system_account.account_type:
				return 1
			else:
				return 2	
	except:
		return 1

# auth on page for profile
@render_to('profile/auth.html')
def auth(request):
	result = ''
	if request.method == 'POST' and request.POST:
		password = hashlib.md5()
		password.update(request.POST['password'])
		system_account = System_account.objects.filter(email=request.POST['email'], password=password.hexdigest())	
		try: 
			if system_account[0].email!='' and len(system_account)==1:
				request.session['username'] = system_account[0].email
				if system_account[0].account_type:
					return HttpResponseRedirect("/lender/account/")
				else:
					return HttpResponseRedirect("/profile/")
		except:
			result = 'Wrong Username/Email and password combination.'
	return {'request': request, 'result': result}

# profile client
@render_to('profile/apply.html')
def profile(request):
	if check_auth(request)==0:
	    return HttpResponseRedirect("/auth/")
	elif check_auth(request)==1:
	    return HttpResponseRedirect("/lender/account/")

	system_account = System_account.objects.get(email=request.session['username'])
	business = Business.objects.get(system_account=system_account.id)
	borrower = Borrower.objects.get(system_account=system_account.id)
	if borrower.accepted:
	    return HttpResponseRedirect("/account/finish")
	try:
		business_measure.amount = request.GET['amount'] + "000"
		business_measure.save()
	except:
		business_measure = Business_measure.objects.get(system_account=system_account.id)
	return {'request': request, 'system_account': system_account, 'borrower':borrower, 'business':business, 'business_measure':business_measure}

# qualify
@render_to('profile/qualify.html')
def qualify(request):
	if check_auth(request)==0:
	    return HttpResponseRedirect("/auth/")
	elif check_auth(request)==1:
	    return HttpResponseRedirect("/lender/account/")

	system_account = System_account.objects.get(email=request.session['username'])
	business_measure = Business_measure.objects.get(system_account=system_account.id)
	return {'request': request, 'business_measure':business_measure}

# finish
@render_to('profile/finish.html')
def finish_page(request):
	if check_auth(request)==0:
	    return HttpResponseRedirect("/auth/")
	elif check_auth(request)==1:
	    return HttpResponseRedirect("/lender/account/")
	return {'request': request}

# accepted
@render_to('profile/accepted.html')
def accepted(request):
	if check_auth(request)==0:
	    return HttpResponseRedirect("/auth/")
	elif check_auth(request)==1:
	    return HttpResponseRedirect("/lender/account/")

	system_account = System_account.objects.get(email=request.session['username'])
	business = Business.objects.get(system_account=system_account.id)
	borrower = Borrower.objects.get(system_account=system_account.id)
	if borrower.accepted:
	    return HttpResponseRedirect("/account/finish")
	bank_file = Bank_file.objects.filter(system_account=system_account.id)
	processor_file = Processor_file.objects.filter(system_account=system_account.id)
	financial_file =  Financial_file.objects.filter(system_account=system_account.id)


	if request.method == 'POST' and request.POST:
		business.ein = request.POST['ein']
		business.save()
		borrower.ssn = request.POST['ssn']
		borrower.save()


	return {'request': request,
			'business':business, 
			'borrower':borrower, 
			'bank_file':bank_file, 
			'processor_file':processor_file, 
			'financial_file':financial_file}


# credit offers for profile
@render_to('profile/credit-offers.html')
def credit_offers(request):
	if check_auth(request)==0:
	    return HttpResponseRedirect("/auth/")
	elif check_auth(request)==1:
	    return HttpResponseRedirect("/lender/account/")

	system_account = System_account.objects.get(email=request.session['username'])
	borrower = Borrower.objects.get(system_account=system_account.id)
	result = Loan_offer.objects.filter(borrower=borrower, enable=True)
	lists = []
	for value in result:
		lists.append(dict([('amount', value.amount),
						   ('id', value.id),
						   ('repaid_amount', value.repaid_amount),
						   ('lender', value.lender.id),
						   ('daily_repayment_sale', value.daily_repayment_sale),
						   ('status', value.status_lender),
						   ('company', value.lender.company)]))
	return {'request': request, 'lists': lists}	

# account for profile
@render_to('profile/account.html')
def account(request):
	if check_auth(request)==0:
	    return HttpResponseRedirect("/auth/")
	elif check_auth(request)==1:
	    return HttpResponseRedirect("/lender/account/")

	system_account = System_account.objects.get(email=request.session['username'])
	borrower = Borrower.objects.get(system_account=system_account.id)
	business = Business.objects.get(system_account=system_account.id)
	business_measure = Business_measure.objects.get(system_account=system_account.id)
	bank_file = Bank_file.objects.filter(system_account=system_account.id)
	processor_file = Processor_file.objects.filter(system_account=system_account.id)
	financial_file =  Financial_file.objects.filter(system_account=system_account.id)
	return {'request': request, 'bank_file':bank_file, 'financial_file':financial_file, 'processor_file':processor_file, 'system_account': system_account, 'business':business, 'borrower':borrower, 'business_measure': business_measure}

# statements for profile
@render_to('profile/statements.html')
def statements(request):
	if check_auth(request)==0:
	    return HttpResponseRedirect("/auth/")
	elif check_auth(request)==1:
	    return HttpResponseRedirect("/lender/account/")

	return {'request': request}

# save data for profile page
def save_profile_main(request):
	if check_auth(request)==0:
	    return HttpResponseRedirect("/auth/")
	elif check_auth(request)==1:
	    return HttpResponseRedirect("/lender/account/")

	system_account = System_account.objects.get(email=request.session['username'])
	borrower = Borrower.objects.get(system_account=system_account.id)
	borrower.suffix = request.GET['suffix']
	borrower.first_name = request.GET['first_name']
	borrower.middle_name = request.GET['middle_name']
	borrower.last_name = request.GET['last_name']
	borrower.other_name = request.GET['other_name']
	borrower.street = request.GET['street']
	borrower.city = request.GET['city']
	try: 
		state=State.objects.get(name=request.GET['state'])
		borrower.state=state
	except:
		borrower.state = ''
	borrower.zip_code = request.GET['zip_code']
	try: 
		country=Country.objects.get(name=request.GET['country'])
		borrower.country=country
	except:
		client.country = ''	
	borrower.home_phone = request.GET['home_phone']
	borrower.cell_phone = request.GET['cell_phone']
	borrower.date_of_birth = request.GET['date_of_birth']
	borrower.save()
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# save data for profile business page
def save_profile_business(request):
	if check_auth(request)==0:
	    return HttpResponseRedirect("/auth/")
	elif check_auth(request)==1:
	    return HttpResponseRedirect("/lender/account/")

	system_account = System_account.objects.get(email=request.session['username'])
	business = Business.objects.get(system_account=system_account.id)
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
	if check_auth(request)==0:
	    return HttpResponseRedirect("/auth/")
	elif check_auth(request)==1:
	    return HttpResponseRedirect("/lender/account/")

	system_account = System_account.objects.get(email=request.session['username'])
	business_measure = Business_measure.objects.get(system_account=system_account.id)
	business_measure.amount = int(request.GET['amount'])
	business_measure.monthly_sales = int(request.GET['monthly_sales'])
	business_measure.revenue = int(request.GET['revenue'])
	if request.GET['profit']!='':
		business_measure.net_profit = int(request.GET['profit'])
	else:
		business_measure.net_profit = 0
	business_measure.save()
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# finish account
def account_finish(request):
	if check_auth(request)==0:
	    return HttpResponseRedirect("/auth/")
	elif check_auth(request)==1:
	    return HttpResponseRedirect("/lender/account/")

	system_account = System_account.objects.get(email=request.session['username'])

	if settings.PROD:
		send_mail(const.FINISH_APPLICATION_THEMA, const.FINISH_APPLICATION_TEXT+' '+str(request.session['username']), const.EMAIL_FROM, [const.FINISH_APPLICATION_EMAIL, const.FINISH_APPLICATION_EMAIL_COPY], fail_silently=False)	

	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )	

# save files
@csrf_exempt
def save_files(request):
	system_account = System_account.objects.get(email=request.session['username'])
	anchor = ''
	try:
		bank_file = Bank_file()
		bank_file.system_account = system_account
		bank_file.bank_file = request.FILES['bank_file']
		bank_file.save()
		anchor = '#bank'
	except:
		request.FILES['bank_file'] = ''

	try:
		financial_file = Financial_file()
		financial_file.system_account = system_account
		financial_file.financial_file = request.FILES['financial_file']
		financial_file.save()
		anchor = '#financial'
	except:
		request.FILES['financial_file'] = ''

	try:
		processor_file = Processor_file()
		processor_file.system_account = system_account
		processor_file.processor_file = request.FILES['processor_file']
		processor_file.save()
		anchor = '#processor'
	except:
		request.FILES['processor_file'] = ''

	return HttpResponseRedirect("/profile/accepted/"+str(anchor))

# remove bank file
def remove_bank_file(request, id):
	bank_file = Bank_file.objects.get(pk=id)
	if str(bank_file.system_account) == request.session['username']:
		bank_file.delete()
	return HttpResponseRedirect("/profile/accepted/#bank")

# remove processor file
def remove_processor_file(request, id):
	processor_file = Processor_file.objects.get(pk=id)
	if str(processor_file.system_account) == request.session['username']:
		processor_file.delete()
	return HttpResponseRedirect("/profile/accepted/#processor")

# remove financial file
def remove_financial_file(request, id):
	financial_file = Financial_file.objects.get(pk=id)
	if str(financial_file.system_account) == request.session['username']:
		financial_file.delete()
	return HttpResponseRedirect("/profile/accepted/#financial")

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

# get risk level
def get_risk_level(request):
	if check_auth(request):
		return HttpResponseRedirect("/auth/")
	result = Risk_level.objects.all()
	categories = []
	for category in result:
		categories.append(category.name)	
	return HttpResponse( json.dumps({'categories':categories}), mimetype="application/json" )
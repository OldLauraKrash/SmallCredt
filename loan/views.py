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


# loan accepted
def loan_accepted(request):
	loan_offer = Loan_offer.objects.get(id=request.GET['id'])
	loan_offer.status_lender = 1
	loan_offer.enable = True
	loan_offer.save()

	business = Business.objects.get(system_account=loan_offer.lender.system_account.id)	
	loan = Loan()
	loan.loan_offer = loan_offer
	loan.amount = loan_offer.amount
	loan.lender = loan_offer.lender
	loan.daily_repayment_sale = loan_offer.daily_repayment_sale
	loan.bussiness = business
	loan_offer.enable = True
	loan.remaining_balance = 0
	loan.save()

	if settings.PROD:	
		send_mail(const.LOAN_THEMA, const.LOAN_TEXT, const.EMAIL_FROM, [loan_offer.lender.system_account.email], fail_silently=False)
		#send_mail(const.LOAN_THEMA, const.LOAN_TEXT, const.EMAIL_FROM, [loan_offer.borrower.system_account.email], fail_silently=False)	
	
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )

# loan cancel
def loan_cancel(request):
	loan_offer = Loan_offer.objects.get(id=request.GET['id'])
	loan_offer.enable = False
	loan_offer.save()

	try:
		loan = Loan.objects.get(loan_offer=loan_offer)
		loan.enable = False
		loan.save()
	except:
		loan = ''
	if settings.PROD:	
		send_mail(const.LOAN_THEMA, const.LOAN_TEXT, const.EMAIL_FROM, [loan_offer.lender.system_account.email], fail_silently=False)			
		#send_mail(const.LOAN_THEMA, const.LOAN_TEXT, const.EMAIL_FROM, [loan_offer.borrower.system_account.email], fail_silently=False)
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )	

# loan decline
def loan_decline(request):
	loan_offer = Loan_offer.objects.get(id=request.GET['id'])
	loan_offer.status_lender = 2
	loan_offer.enable = True
	loan_offer.save()
	if settings.PROD:
		send_mail(const.LOAN_THEMA, const.LOAN_TEXT, const.EMAIL_FROM, [loan_offer.lender.system_account.email], fail_silently=False)
		#send_mail(const.LOAN_THEMA, const.LOAN_TEXT, const.EMAIL_FROM, [loan_offer.borrower.system_account.email], fail_silently=False)		
	return HttpResponse( json.dumps({'result':'ok'}), mimetype="application/json" )
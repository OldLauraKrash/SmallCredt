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
from django.views.decorators.csrf import csrf_exempt


# profile lender
@render_to('lender/account.html')
def lender_account(request):
	return {}

# statements lender
@render_to('lender/statements.html')
def lender_statements(request):
	return {}

# portfolio lender
@render_to('lender/portfolio.html')
def lender_portfolio(request):
	return {}

# edit lender
@render_to('lender/edit.html')
def lender_edit(request):
	return {}

# marketplace lender
@render_to('lender/marketplace.html')
def lender_marketplace(request):
	return {}
# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to 
from client.models import *
import hashlib
import simplejson as json
from django.http import HttpResponseRedirect
import const
from django.core.mail import send_mail
from django.conf import settings
import time

# main page
@render_to('main/index.html')
def home(request):
	'''
	Home page

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`

	**Template:**

	:template:`main/main.html`
	'''
	active = False
	try:
		if request.session['username'] != '':
			active = True
	except:
		active = False
	return {'request': request, 'active':active}

# sign in client
def login(request):
	'''
	Sign in

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`
	'''
	lender = 0
	result = 'error'
	password = hashlib.md5()
	password.update(request.GET['password'])
	system_account = System_account.objects.filter(email=request.GET['email'], password=password.hexdigest())	
	try: 
		if system_account[0].email!='' and len(system_account)==1:
			request.session['username'] = system_account[0].email
			if system_account[0].account_type:
				lender = 1
			else:
				lender = 0
			result = 'ok'
	except:
		result = 'error'
	return HttpResponse( json.dumps({'result':result, 'lender':lender}), mimetype="application/json" )

# sign up client
def register(request):
	'''
	Sign up

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`
	'''
	# save client
	password = hashlib.md5()
	password.update(request.GET['password'])
	ticket = hashlib.md5()
	ticket.update(request.GET['password']+request.GET['email'])
	system_account = System_account(email=request.GET['email'], password=password.hexdigest(), ticket= ticket.hexdigest())
	try:
		system_account.save()
	except:
		return HttpResponse( json.dumps({'result':'error'}), mimetype="application/json" )

	# save param borrower
	borrower = Borrower()
	borrower.system_account=system_account
	borrower.save()

	# save param Business
	business = Business()
	business.system_account=system_account
	business.save()

	# save param Business measure
	business_measure = Business_measure()
	business_measure.system_account=system_account
	business_measure.preliminary_offer = 0
	business_measure.amount = request.GET['amount'] + "000"
	business_measure.save()

	# send message on email
	request.session['username'] = system_account.email
	if settings.PROD:
		send_mail(const.REGISTER_THEMA_EMAIL, const.REGISTER_TEXT_EMAIL+system_account.ticket, const.EMAIL_FROM, [system_account.email], fail_silently=False)
	return HttpResponse( json.dumps({'result':'ok', 'username':system_account.email}), mimetype="application/json" )

# send link on change password
def forget_send(request):
	'''
	Send forget password

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`
	'''
	if settings.PROD:
		try:
			system_account = System_account.objects.get(email=request.GET['email'])	
			send_mail(const.FORGET_THEMA_EMAIL, const.FORGET_TEXT_EMAIL+system_account.ticket, const.EMAIL_FROM, [system_account.email], fail_silently=False)	
		except:
			return HttpResponse( json.dumps({'result':'error'}))		
	return HttpResponse( json.dumps({'result':'ok'}))

# forget password
@render_to('main/forget.html')
def forget(request, ticket):
	'''
	Reset password page

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`

	**Template:**

	:template:`main/forget.html`
	'''
	try:
		system_account = System_account.objects.get(ticket=ticket)
	except:
		return HttpResponseRedirect("/")
			
	if request.method == 'POST' and request.POST:
		hash_ticket = hashlib.md5()
		hash_ticket.update(ticket)
		system_account = System_account.objects.get(ticket=ticket)
		password = hashlib.md5()
		password.update(request.POST['password'])
		system_account.password = password.hexdigest()
		system_account.ticket = hash_ticket.hexdigest()
		system_account.save()
		return HttpResponseRedirect("/")

	return {'request': request, 'ticket': ticket}

# active account
def active_account(request, ticket):
	'''
	Active account

	**Context**

	``request`` 
	``ticket`` - ticket hash

	``models``

	    An instance of :model:`client.System_account`
	'''
	hash_ticket = hashlib.md5()
	hash_ticket.update(ticket)
	try:
		system_account = System_account.objects.get(ticket=ticket)
		system_account.status=True
		system_account.ticket = hash_ticket.hexdigest()
		system_account.save()
		request.session['username'] = system_account.email
		return HttpResponseRedirect("/profile")
	except:
		return HttpResponseRedirect("/")	

# logout for profile
def logout(request):
	'''
	Logout

	**Context**

	``request``

	``models``

	    An instance of :model:`client.System_account`
	'''
	request.session['username']=''
	return HttpResponseRedirect("/")
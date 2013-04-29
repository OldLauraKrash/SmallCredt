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

# main page
@render_to('main/index.html')
def home(request):
	active = False
	try:
		if request.session['username'] != '':
			active = True
	except:
		active = False
	return {'request': request, 'active':active}

# sign in client
def login(request):
	result = 'error'
	password = hashlib.md5()
	password.update(request.GET['password'])
	client = Client.objects.filter(email=request.GET['email'], password=password.hexdigest())	
	try: 
		if client[0].email!='' and len(client)==1:
			request.session['username'] = client[0].email
			result = 'ok'
	except:
		result = 'error'
	return HttpResponse( json.dumps({'result':result}), mimetype="application/json" )

# sign up client
def register(request):
	# save client
	password = hashlib.md5()
	password.update(request.GET['password'])
	ticket = hashlib.md5()
	ticket.update(request.GET['password']+request.GET['email'])
	client = Client(email=request.GET['email'], password=password.hexdigest(), ticket= ticket.hexdigest())
	client.save()
	# save param business
	business = Business()
	business.client=client
	business.save()
	# save param credit
	credit = Loan_offer()
	credit.client=client
	credit.save()
	# send message on email
	request.session['username'] = client.email
	if settings.PROD:
		send_mail(const.REGISTER_THEMA_EMAIL, const.REGISTER_TEXT_EMAIL+client.ticket, const.EMAIL_FROM, [client.email], fail_silently=False)
	return HttpResponse( json.dumps({'result':'ok', 'username':client.email}), mimetype="application/json" )

# send link on change password
def forget_send(request):
	if settings.PROD:
		try:
			client = Client.objects.get(email=request.GET['email'])	
			send_mail(const.FORGET_THEMA_EMAIL, const.FORGET_TEXT_EMAIL+client.ticket, const.EMAIL_FROM, [client.email], fail_silently=False)	
		except:
			return HttpResponse( json.dumps({'result':'error'}))		
	return HttpResponse( json.dumps({'result':'ok'}))

# forget password
@render_to('main/forget.html')
def forget(request, ticket):
	try:
		client = Client.objects.get(ticket=ticket)
	except:
		return HttpResponseRedirect("/")
			
	if request.method == 'POST' and request.POST:
		client = Client.objects.get(ticket=ticket)
		password = hashlib.md5()
		password.update(request.POST['password'])
		client.password = password.hexdigest()
		client.save()
		return HttpResponseRedirect("/")

	return {'request': request, 'ticket': ticket}

# active account
def active_account(request, ticket):
	try:
		client = Client.objects.get(ticket=ticket)
		client.enable=True
		client.save()
		request.session['username'] = client.email
		return HttpResponseRedirect("/profile")
	except:
		return HttpResponseRedirect("/")	

# logout for profile
def logout(request):
	request.session['username']=''
	return HttpResponseRedirect("/")
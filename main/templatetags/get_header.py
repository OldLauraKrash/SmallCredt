# -*- coding: utf-8 -*
from django import template
from client.models import *

register = template.Library()
@register.inclusion_tag('main/header_right.html') 
def get_header_right(request):
	username = ''
	flag = True
	lender = ''
	try:
		if request.session['username']!='':
			username = request.session['username']
			system_account = System_account.objects.get(email=request.session['username'])
			if system_account.account_type:
				lender = request.session['username']
			else:
				lender = ''				
			flag = Flase
	except:
		flag = True
		lender = ''
	return {'flag': flag, 'request': request, 'username': username, 'lender':lender}


@register.inclusion_tag('main/menu_flatpages.html') 
def menu_flatpages(request):
	flag = True
	try:
		system_account = System_account.objects.get(email=request.session['username'])
		if system_account.account_type:
			flag = False
		else:
			flag = True
	except:
		system_account = ''
	return {'request': request, 'system_account':system_account, 'flag': flag}
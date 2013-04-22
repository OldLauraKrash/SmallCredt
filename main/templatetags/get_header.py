# -*- coding: utf-8 -*
from django import template

register = template.Library()
@register.inclusion_tag('main/header_right.html') 
def get_header_right(request):
	username = ''
	flag = False
	try:
		if request.session['username']!='':
			username = request.session['username']
			flag = True
	except:
		flag = False

	return {'flag': flag, 'request': request, 'username': username}
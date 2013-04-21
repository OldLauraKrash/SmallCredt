# -*- coding: utf-8 -*
from django import template

register = template.Library()
@register.inclusion_tag('main/header_right.html', takes_context = True) 
def get_header_right(context):
	return {'flag':False}
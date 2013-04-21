# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to 
from client.models import *
import hashlib
import simplejson as json

@render_to('profile/apply.html')
def profile(request):
	return {}

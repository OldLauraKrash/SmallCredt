# -*- coding: utf-8 -*
from django.http import HttpResponse
from annoying.decorators import render_to


# register account through api step first
@render_to('api/register_step_first.html')
def register_step_first(request):
    '''
	Register account through api step 1

	**Context**

	``request``

	**Template:**

	:template:`api/register_step_first.html`
	'''
    return {'request': request}

# register account through api step second
@render_to('api/register_step_second.html')
def register_step_second(request):
    '''
	Register account through api step 2

	**Context**

	``request``

	**Template:**

	:template:`api/register_step_first.html`
	'''
    return {'request': request}

# register account through api step finish
@render_to('api/register_step_finish.html')
def register_step_finish(request):
    '''
	Register account through api step finish

	**Context**

	``request``

	**Template:**

	:template:`api/register_step_finish.html`
	'''
    return {'request': request}
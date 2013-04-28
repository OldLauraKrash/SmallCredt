# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import generic
from client.models import *

class ClientAdmin(admin.ModelAdmin):
    list_filter = ['created']
    list_display = ('email', 'created', 'enable')
    search_fields = ['email']
    def get_ordering(self, request):
        return ['email']
admin.site.register(Client, ClientAdmin)


class BusinessAdmin(admin.ModelAdmin):
    list_filter = ['client']
    list_display = ['client']
    search_fields = ['client']
    def get_ordering(self, request):
        return ['client']
admin.site.register(Business, BusinessAdmin)

class Loan_offerAdmin(admin.ModelAdmin):
    list_filter = ['client']
    list_display = ['client']
    search_fields = ['client']
    def get_ordering(self, request):
        return ['client']
admin.site.register(Loan_offer, Loan_offerAdmin)
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import generic
from loan.models import *

class Loan_offerAdmin(admin.ModelAdmin):
    list_filter = ['lender']
    list_display = ['lender']
    search_fields = ['lender']
    def get_ordering(self, request):
        return ['lender']
admin.site.register(Loan_offer, Loan_offerAdmin)

class LoanAdmin(admin.ModelAdmin):
    list_filter = ['bussiness']
    list_display = ['bussiness']
    search_fields = ['bussiness']
    def get_ordering(self, request):
        return ['bussiness']
admin.site.register(Loan, LoanAdmin)

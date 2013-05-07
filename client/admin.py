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

class LegalAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name']
    search_fields = ['name']
    def get_ordering(self, request):
        return ['name']
admin.site.register(Legal, LegalAdmin)

class StateAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name']
    search_fields = ['name']
    def get_ordering(self, request):
        return ['name']
admin.site.register(State, StateAdmin)

class IndustryAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name']
    search_fields = ['name']
    def get_ordering(self, request):
        return ['name']
admin.site.register(Industry, IndustryAdmin)

class CountryAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name']
    search_fields = ['name']
    def get_ordering(self, request):
        return ['name']
admin.site.register(Country, CountryAdmin)

class BankAdmin(admin.ModelAdmin):
    list_filter = ['client']
    list_display = ['client']
    search_fields = ['client']
    def get_ordering(self, request):
        return ['client']
admin.site.register(Bank, BankAdmin)
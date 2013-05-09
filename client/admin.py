# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import generic
from client.models import *

class System_accountAdmin(admin.ModelAdmin):
    list_filter = ['created']
    list_display = ('email', 'created', 'status')
    search_fields = ['email']
    def get_ordering(self, request):
        return ['email']
admin.site.register(System_account, System_accountAdmin)


class BorrowerAdmin(admin.ModelAdmin):
    list_filter = ['system_account']
    list_display = ['system_account']
    search_fields = ['system_account']
    def get_ordering(self, request):
        return ['system_account']
admin.site.register(Borrower, BorrowerAdmin)

class BusinessAdmin(admin.ModelAdmin):
    list_filter = ['system_account']
    list_display = ['system_account']
    search_fields = ['system_account']
    def get_ordering(self, request):
        return ['system_account']
admin.site.register(Business, BusinessAdmin)

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

class Business_measureAdmin(admin.ModelAdmin):
    list_filter = ['system_account']
    list_display = ['system_account']
    search_fields = ['system_account']
    def get_ordering(self, request):
        return ['system_account']
admin.site.register(Business_measure, Business_measureAdmin)
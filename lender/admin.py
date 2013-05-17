# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import generic
from lender.models import *

class LenderAdmin(admin.ModelAdmin):
    list_filter = ['system_account']
    list_display = ['system_account']
    search_fields = ['system_account']
    def get_ordering(self, request):
        return ['system_account']
admin.site.register(Lender, LenderAdmin)

class GeographyAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name']
    search_fields = ['name']
    def get_ordering(self, request):
        return ['name']
admin.site.register(Geography, GeographyAdmin)

class RiskAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name']
    search_fields = ['name']
    def get_ordering(self, request):
        return ['name']
admin.site.register(Risk, RiskAdmin)


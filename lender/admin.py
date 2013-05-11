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
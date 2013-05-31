# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import generic
from api.models import *

class InstitutionAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name']
    search_fields = ['name']
    def get_ordering(self, request):
        return ['name']
admin.site.register(Institution, InstitutionAdmin)
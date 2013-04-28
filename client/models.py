# -*- coding: utf-8 -*-
from django.db import models

class Client(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    ticket = models.CharField(max_length=255) 
    suffix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    other_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    home_phone = models.CharField(max_length=255)
    cell_phone = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField(null=True)
    enable = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)	
    def __unicode__(self):
        return unicode(self.email)

class Business(models.Model):
    business_name = models.CharField(max_length=255)
    dba = models.CharField(max_length=255)
    legal_form = models.CharField(max_length=255)
    state_of_incorporation = models.CharField(max_length=255)
    date_founded = models.DateTimeField(null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    business_phone = models.CharField(max_length=255)
    industry = models.CharField(max_length=255) 
    client = models.ForeignKey(Client)
    def __unicode__(self):
        return unicode(self.client)

class Loan_offer(models.Model):
    amount = models.CharField(max_length=255)
    monthly_sales = models.CharField(max_length=255)
    revenue = models.CharField(max_length=255)
    net_profit = models.CharField(max_length=255)
    client = models.ForeignKey(Client)
    def __unicode__(self):
        return unicode(self.client)	

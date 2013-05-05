# -*- coding: utf-8 -*-
from django.db import models

class Legal(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return unicode(self.name)

class State(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return unicode(self.name)

class Industry(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return unicode(self.name)

class Country(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return unicode(self.name)

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
    state = models.ForeignKey(State, null=True)
    zip_code = models.CharField(max_length=255)
    country = models.ForeignKey(Country, null=True)
    home_phone = models.CharField(max_length=255)
    cell_phone = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField(null=True)
    enable = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)   
    def __unicode__(self):
        return unicode(self.email)

def get_dir(instance, filename):
    return u'uploads/%s/%s' % (instance.id, filename)

class Bank(models.Model):
    social_security_number = models.CharField(max_length=15)
    ein = models.CharField(max_length=15)
    bank_name = models.CharField(max_length=255)
    bank_username = models.CharField(max_length=255)
    bank_password = models.CharField(max_length=255)
    financial_file = models.FileField(upload_to=get_dir)
    processor_name = models.CharField(max_length=255)
    processor_username = models.CharField(max_length=255)
    processor_password = models.CharField(max_length=255)
    client = models.ForeignKey(Client)
    def __unicode__(self):
        return unicode(self.client)

class Business(models.Model):
    business_name = models.CharField(max_length=255)
    dba = models.CharField(max_length=255)
    legal_form = models.ForeignKey(Legal, null=True)
    state_of_incorporation = models.ForeignKey(State, null=True, related_name='state_of_incorporation')
    date_founded = models.DateTimeField(null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.ForeignKey(State, null=True, related_name='state')
    zip_code = models.CharField(max_length=255)
    country = models.ForeignKey(Country, null=True)
    business_phone = models.CharField(max_length=255)
    industry = models.ForeignKey(Industry, null=True)
    client = models.ForeignKey(Client)
    def __unicode__(self):
        return unicode(self.client)

class Loan_offer(models.Model):
    preliminary_offer = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    monthly_sales = models.IntegerField(blank=True, null=True)
    revenue = models.IntegerField(blank=True, null=True)
    net_profit = models.IntegerField(blank=True, null=True)
    client = models.ForeignKey(Client)
    def __unicode__(self):
        return unicode(self.client)	


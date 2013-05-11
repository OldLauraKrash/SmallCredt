# -*- coding: utf-8 -*-
from django.db import models
from time import gmtime, strftime

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

class System_account(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    ticket = models.CharField(max_length=255) 
    account_type = models.BooleanField(verbose_name="Lender")
    status = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)   
    def __unicode__(self):
        return unicode(self.email)

class Borrower(models.Model): 
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
    ssn = models.CharField(max_length=15)
    borrower_status = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    system_account = models.ForeignKey(System_account)   
    def __unicode__(self):
        return unicode(self.system_account)

class Business(models.Model):
    business_name = models.CharField(max_length=255)
    dba = models.CharField(max_length=255)
    ein = models.CharField(max_length=15)
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
    system_account = models.ForeignKey(System_account)
    def __unicode__(self):
        return unicode(self.system_account)

def get_dir(instance, filename):
    return u'uploads/%s/%s' % (instance.system_account, strftime("%Y-%m-%d %H:%M:%S", gmtime())+'-'+str(filename))

class Bank_file(models.Model):
    system_account = models.ForeignKey(System_account)
    bank_file = models.FileField(upload_to=get_dir)
    def __unicode__(self):
        return unicode(self.system_account) 

class Financial_file(models.Model):
    system_account = models.ForeignKey(System_account)
    financial_file = models.FileField(upload_to=get_dir)
    def __unicode__(self):
        return unicode(self.system_account) 

class Processor_file(models.Model):
    system_account = models.ForeignKey(System_account)
    processor_file = models.FileField(upload_to=get_dir)
    def __unicode__(self):
        return unicode(self.system_account)

class Business_measure(models.Model):
    preliminary_offer = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    monthly_sales = models.IntegerField(blank=True, null=True)
    revenue = models.IntegerField(blank=True, null=True)
    net_profit = models.IntegerField(blank=True, null=True)
    system_account = models.ForeignKey(System_account)
    def __unicode__(self):
        return unicode(self.system_account)	


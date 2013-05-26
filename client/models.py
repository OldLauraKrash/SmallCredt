# -*- coding: utf-8 -*-
from django.db import models
from time import gmtime, strftime
import hashlib

class Risk_level(models.Model):
    """
    The level of the risk for the borrower, related to :model:`client.Borrower`
    """
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return unicode(self.name)

class Legal(models.Model):
    """
    Legal, related to :model:`client.Business`
    """
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return unicode(self.name)

class State(models.Model):
    """
    States in the country, related to :model:`client.Borrower` and :model:`client.Business`
    """
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return unicode(self.name)

class Industry(models.Model):
    """
    A industries list, related to :model:`client.Business`
    """
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return unicode(self.name)

class Country(models.Model):
    """
    A countries list, related to :model:`client.Borrower` and :model:`client.Business`
    """
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return unicode(self.name)

class System_account(models.Model):
    """
    Main account, related to :model:`client.Borrower`, :model:`client.Business`, :model:`client.Bank_file`, :model:`client.Financial_file`,
    :model:`client.Processor_file` and :model:`client.Business_measure`
    """
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    ticket = models.CharField(max_length=255, null=True, blank=True) 
    account_type = models.BooleanField(verbose_name="Lender")
    status = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)   
    def __unicode__(self):
        return unicode(self.email)

class Borrower(models.Model):
    """
    Borrower account, related to :model:`client.Risk_level`, :model:`client.Business`, :model:`client.System_account`, 
    :model:`client.State` and :model:`client.Country` 
    """ 
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
    risk_level = models.ForeignKey(Risk_level, null=True)
    accepted = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    system_account = models.ForeignKey(System_account)   
    def __unicode__(self):
        return unicode(self.system_account)

class Business(models.Model):
    """
    Business information for the borrower, related to :model:`client.State`, :model:`client.System_account` and  :model:`client.Country` 
    """
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

# get path for saving file
def get_dir(instance, filename):
    # hash for first folder
    account = hashlib.md5()
    account.update(str(instance.system_account))
    account = str(account.hexdigest())   
    # hash for second folder
    created = hashlib.md5()
    created.update(str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    created = str(created.hexdigest())  
    # return full path
    return u'uploads/%s/%s/%s' % (account, created, str(filename))

class Bank_file(models.Model):
    """
    Bank files, related to :model:`client.System_account`
    """
    system_account = models.ForeignKey(System_account)
    bank_file = models.FileField(upload_to=get_dir, max_length=255)
    def __unicode__(self):
        return unicode(self.system_account) 

class Financial_file(models.Model):
    """
    Financial files, related to :model:`client.System_account`
    """
    system_account = models.ForeignKey(System_account)
    financial_file = models.FileField(upload_to=get_dir, max_length=255)
    def __unicode__(self):
        return unicode(self.system_account) 

class Processor_file(models.Model):
    """
    Processor files, related to :model:`client.System_account`
    """
    system_account = models.ForeignKey(System_account)
    processor_file = models.FileField(upload_to=get_dir, max_length=255)
    def __unicode__(self):
        return unicode(self.system_account)

class Business_measure(models.Model):
    """
    Business measure inforamtion for the borrower, related to :model:`client.System_account`
    """
    preliminary_offer = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    monthly_sales = models.IntegerField(blank=True, null=True)
    revenue = models.IntegerField(blank=True, null=True)
    net_profit = models.IntegerField(blank=True, null=True)
    system_account = models.ForeignKey(System_account)
    def __unicode__(self):
        return unicode(self.system_account)	


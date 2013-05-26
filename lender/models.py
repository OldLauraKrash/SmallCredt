from django.db import models
from client.models import *

class Geography(models.Model):
    """
    A geographical list, related to :model:`lender.Lender`
    """    
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return unicode(self.name)

class Risk(models.Model):
    """
    The level of the risk for the lender, related to :model:`lender.Lender`
    """
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return unicode(self.name)
        
class Lender(models.Model): 
    """
    Infromation about the lender, related to :model:`client.State`, :model:`client.Country`, :model:`lender.Geography` and
    :model:`lender.Risk`
    """
    suffix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    home_phone = models.CharField(max_length=255)
    cell_phone = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.ForeignKey(State, null=True)
    zip_code = models.CharField(max_length=255)
    country = models.ForeignKey(Country, null=True)
    lender_status = models.BooleanField()
    industry = models.ForeignKey(Industry, null=True)
    geography = models.ForeignKey(Geography, null=True)
    created = models.DateTimeField(auto_now_add=True)
    risk = models.ForeignKey(Risk, null=True)
    system_account = models.ForeignKey(System_account)   
    def __unicode__(self):
        return unicode(self.system_account)


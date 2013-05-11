from django.db import models
from client.models import *

class Lender(models.Model): 
    suffix = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    home_phone = models.CharField(max_length=255)
    cell_phone = models.CharField(max_length=255)
    lender_status = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    system_account = models.ForeignKey(System_account)   
    def __unicode__(self):
        return unicode(self.system_account)	

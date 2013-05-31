from django.db import models
from django.contrib.contenttypes import generic
from api.models import *

class Institution(models.Model):
    """
    Institutions list
    """
    aggcat_id = models.IntegerField()
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    def __unicode__(self):
        return unicode(self.name)

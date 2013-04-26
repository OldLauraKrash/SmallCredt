# -*- coding: utf-8 -*-
from django.db import models

class Client(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    ticket = models.CharField(max_length=255) 
    enable = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
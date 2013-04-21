# -*- coding: utf-8 -*-
from django.db import models

class Client(models.Model):
    email = models.EmailField(max_length=255, verbose_name="Email")
    password = models.CharField(max_length=255, verbose_name="Password")
    enable = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)


from django.db import models
from client.models import *
from lender.models import *

STATUS= (
    (0, 'Empty'),
    (1, 'Bid'),
    (2, 'Decline'),
)

class Loan_offer(models.Model): 
    lender = models.ForeignKey(Lender)
    borrower = models.ForeignKey(Borrower)
    amount = models.IntegerField(blank=True, null=True)
    repaid_amount = models.IntegerField(blank=True, null=True)
    estimated_repaid_term = models.CharField(max_length=255)
    daily_repayment_sale = models.CharField(max_length=255)
    discount = models.CharField(max_length=255)
    status = models.IntegerField(blank=True, null=True, choices=STATUS)
    offer_date = models.DateTimeField(auto_now_add=True) 
    offer_exp_date = models.DateTimeField(auto_now_add=True)
    status_changed_date = models.DateTimeField(auto_now_add=True)    
    def __unicode__(self):
        return unicode(self.lender) 

class Loan(models.Model):
    bussiness = models.ForeignKey(Business)
    lender = models.ForeignKey(Lender)
    loan_offer = models.ForeignKey(Loan_offer)
    receipt_date  = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(blank=True)
    remaining_balance = models.IntegerField(blank=True)
    credit_rate = models.CharField(max_length=255) 
    repaid_amount = models.CharField(max_length=255)
    repaid_term = models.CharField(max_length=255)
    daily_repayment_sale = models.CharField(max_length=255)
    loan_status = models.BooleanField() 
    def __unicode__(self):
        return unicode(self.bussiness) 

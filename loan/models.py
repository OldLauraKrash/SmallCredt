from django.db import models
from client.models import *
from lender.models import *

STATUS= (
    (1, 'Bid'),
    (2, 'Decline'),
)

STATUS_LENDER= (
    (1, 'Accepted'),
    (2, 'Decline'),
)

class Loan_offer(models.Model): 
    lender = models.ForeignKey(Lender)
    borrower = models.ForeignKey(Borrower)
    amount = models.FloatField(blank=True, null=True)
    repaid_amount = models.FloatField(blank=True, null=True)
    estimated_repaid_term = models.FloatField(blank=True, null=True)
    daily_repayment_sale = models.FloatField(max_length=255)
    discount = models.FloatField(max_length=255)
    status = models.IntegerField(blank=True, null=True, choices=STATUS)
    status_lender = models.IntegerField(blank=True, null=True, choices=STATUS_LENDER)
    offer_date = models.DateTimeField(auto_now_add=True) 
    offer_exp_date = models.DateTimeField(auto_now_add=True)
    status_changed_date = models.DateTimeField(auto_now_add=True)
    enable = models.BooleanField()     
    def __unicode__(self):
        return unicode(self.lender) 

class Loan(models.Model):
    bussiness = models.ForeignKey(Business)
    lender = models.ForeignKey(Lender)
    loan_offer = models.ForeignKey(Loan_offer)
    receipt_date  = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(blank=True)
    remaining_balance = models.FloatField(blank=True)
    credit_rate = models.CharField(max_length=255, null=True) 
    repaid_amount = models.FloatField(max_length=255, null=True)
    repaid_term = models.FloatField(max_length=255, null=True)
    daily_repayment_sale = models.FloatField(max_length=255)
    loan_status = models.BooleanField()
    enable = models.BooleanField() 
    def __unicode__(self):
        return unicode(self.bussiness) 

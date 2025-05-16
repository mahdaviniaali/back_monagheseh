from django.db import models

# Create your models here.

class PurchaseRequest(models.Model):
    pass

class PurchaseRequestAttachment(models.Model):
    purchase_request = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE, related_name='attachments')


from django.db import models

# Create your models here.
# **Payment**
# **Invoice**
# **TransactionLog**

class Payment(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} - {self.status}"

class Invoice(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='invoices')
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for {self.user.username} - {self.status}"
    
class TransactionLog(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transaction_logs')
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failure', 'Failure')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} for {self.payment.user.username} - {self.status}"
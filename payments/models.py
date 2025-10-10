from django.db import models
from django.core.validators import MinValueValidator

class Payment(models.Model):
    """Payments table - your exact schema"""
    payment_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    datetime = models.DateTimeField(auto_now_add=True)
    tracking_code = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'payments'
        indexes = [
            models.Index(fields=['tracking_code']),
        ]
    
    def __str__(self):
        return f"Payment {self.tracking_code} - ${self.price}"

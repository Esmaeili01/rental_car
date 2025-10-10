from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta
from cars.models import Car
from customers.models import Customer

class Rental(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('overdue', 'Overdue'),
    ]
    
    # Rental Information
    rental_id = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='rentals')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rentals')
    
    # Dates and Times
    pickup_date = models.DateTimeField()
    return_date = models.DateTimeField()
    actual_pickup_date = models.DateTimeField(null=True, blank=True)
    actual_return_date = models.DateTimeField(null=True, blank=True)
    
    # Pricing
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    total_days = models.IntegerField(validators=[MinValueValidator(1)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    insurance_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    additional_fees = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Security Deposit
    security_deposit = models.DecimalField(max_digits=8, decimal_places=2)
    deposit_refunded = models.BooleanField(default=False)
    deposit_refund_date = models.DateTimeField(null=True, blank=True)
    
    # Vehicle Condition
    pickup_mileage = models.IntegerField(default=0)
    return_mileage = models.IntegerField(null=True, blank=True)
    pickup_fuel_level = models.CharField(max_length=20, default='Full')
    return_fuel_level = models.CharField(max_length=20, blank=True)
    
    # Status and Notes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    pickup_notes = models.TextField(blank=True)
    return_notes = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    # Staff Information
    pickup_staff = models.CharField(max_length=255, blank=True)
    return_staff = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.rental_id:
            # Generate unique rental ID
            import uuid
            self.rental_id = f"RNT-{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate total days
        if self.pickup_date and self.return_date:
            delta = self.return_date.date() - self.pickup_date.date()
            self.total_days = max(1, delta.days)
        
        # Calculate subtotal
        self.subtotal = self.daily_rate * self.total_days
        
        # Calculate total amount
        self.total_amount = self.subtotal + self.tax_amount + self.insurance_amount + self.additional_fees
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Rental {self.rental_id} - {self.customer.full_name} - {self.car.full_name}"
    
    @property
    def is_overdue(self):
        if self.status == 'active' and self.return_date:
            return timezone.now() > self.return_date
        return False
    
    @property
    def days_overdue(self):
        if self.is_overdue:
            return (timezone.now().date() - self.return_date.date()).days
        return 0
    
    @property
    def duration_in_days(self):
        if self.actual_pickup_date and self.actual_return_date:
            return (self.actual_return_date.date() - self.actual_pickup_date.date()).days
        return self.total_days
    
    @property
    def total_mileage(self):
        if self.pickup_mileage and self.return_mileage:
            return self.return_mileage - self.pickup_mileage
        return 0
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rental_id']),
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['car', 'pickup_date']),
            models.Index(fields=['status', 'pickup_date']),
        ]

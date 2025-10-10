"""
Django models matching your exact database schema requirements
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    """Users table - simplified user model"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    ]
    
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    birthdate = models.DateField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class Car(models.Model):
    """Cars table with owner relationship"""
    CATEGORY_CHOICES = [
        ('economy', 'Economy'),
        ('compact', 'Compact'),
        ('mid_size', 'Mid-size'),
        ('full_size', 'Full-size'),
        ('premium', 'Premium'),
        ('luxury', 'Luxury'),
        ('suv', 'SUV'),
        ('minivan', 'Minivan'),
        ('sports', 'Sports'),
    ]
    
    GEARBOX_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('cvt', 'CVT'),
    ]
    
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
    ]
    
    car_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_cars')
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=30)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    production_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2030)]
    )
    gearbox = models.CharField(max_length=20, choices=GEARBOX_CHOICES)
    fuel = models.CharField(max_length=20, choices=FUEL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    
    class Meta:
        db_table = 'cars'
        indexes = [
            models.Index(fields=['brand']),
            models.Index(fields=['category']),
            models.Index(fields=['owner']),
        ]
    
    def __str__(self):
        return f"{self.production_year} {self.brand} {self.model} ({self.color})"

class Payment(models.Model):
    """Payments table"""
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

class Rent(models.Model):
    """Rents table"""
    rent_id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.RESTRICT, related_name='rentals')
    renter = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='rentals')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    
    class Meta:
        db_table = 'rents'
        indexes = [
            models.Index(fields=['car']),
            models.Index(fields=['renter']),
            models.Index(fields=['payment']),
            models.Index(fields=['start_datetime', 'end_datetime']),
        ]
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_datetime and self.end_datetime and self.end_datetime <= self.start_datetime:
            raise ValidationError('End datetime must be after start datetime')
    
    def __str__(self):
        return f"Rent {self.rent_id} - {self.car} by {self.renter}"

class Setting(models.Model):
    """Settings table for system configuration"""
    key = models.CharField(max_length=100, primary_key=True)
    value = models.TextField()
    
    class Meta:
        db_table = 'settings'
    
    def __str__(self):
        return f"{self.key}: {self.value}"
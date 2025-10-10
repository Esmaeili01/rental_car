from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from customers.models import User

class Car(models.Model):
    """Cars table - your exact schema"""
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

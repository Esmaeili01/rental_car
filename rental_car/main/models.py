from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "superadmin")
        user = self.create_user(email, password, **extra_fields)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    last_login = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    birthdate = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    address = models.TextField(null=True, blank=True)
    role = models.CharField(
        max_length=15,
        choices=[('superadmin','Super Admin'), ('admin','Admin'), ('owner','Owner'), ('renter','Renter')],
        default='renter'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = UserManager()
    
    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email



class Car(models.Model):

    car_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='owner_id')
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    production_year = models.IntegerField()
    color = models.CharField(max_length=20, null=True, blank=True)
    seats = models.IntegerField(null=True, blank=True)
    category = models.CharField(
        max_length=20,
        choices=[
            ('sedan', 'Sedan'),
            ('suv', 'SUV'),
            ('hatchback', 'Hatchback'),
            ('truck', 'Truck'),
            ('van', 'Van'),
        ],
        null=True, blank=True
    )
    only_with_driver = models.BooleanField(null=True, blank=True)
    with_driver = models.BooleanField(null=True, blank=True)
    gearbox = models.CharField(
        max_length=10,
        choices=[('manual', 'Manual'), ('automatic', 'Automatic')],
        null=True, blank=True
    )
    fuel = models.CharField(
        max_length=10,
        choices=[('gasoline', 'Gasoline'), ('diesel', 'Diesel'),
                 ('electric', 'Electric'), ('hybrid', 'Hybrid')],
        null=True, blank=True
    )
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=15,
        choices=[('available', 'Available'), ('suspended', 'Suspended'), ('unavailable', 'Unavailable')],
        default='available'
    )
    country = models.TextField(null=True, blank=True)
    province = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'cars'

    def __str__(self):
        return f"{self.brand} {self.model}"

class Rent(models.Model):

    rent_id = models.AutoField(primary_key=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, db_column='car_id')
    renter_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='renter_id')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending payment', 'Pending Payment'),
            ('on your rent', 'On Your Rent'),
            ('not yet', 'Not Yet'),
            ('over', 'Over')
        ],
        default='pending payment'
    )
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'rents'

    def __str__(self):
        return f"Rent #{self.rent_id} - {self.car}"


class Payment(models.Model):

    payment_id = models.AutoField(primary_key=True)
    rent_id = models.OneToOneField(Rent, on_delete=models.CASCADE, db_column='rent_id')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)
    method = models.CharField(
        max_length=10,
        choices=[('online', 'Online'), ('cash', 'Cash')],
        null=True, blank=True
    )
    tracking_code = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(
        max_length=15,
        choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')],
        default='pending'
    )

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f"Payment #{self.payment_id} - {self.status}"


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    rent_id = models.ForeignKey(Rent, on_delete=models.CASCADE, db_column='rent_id')
    renter_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='renter_id')
    datetime = models.DateTimeField(auto_now_add=True)
    score = models.SmallIntegerField()
    comment = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return f"Review #{self.review_id} - {self.score}/5"
    
class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    is_signup = models.BooleanField()
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'logins'

    def __str__(self):
        return f"{self.user.email} - {'Signup' if self.is_signup else 'Login'} at {self.datetime}"
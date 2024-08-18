from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    arn_number = models.CharField(max_length=20, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['arn_number']

    objects = UserManager()

    def __str__(self):
        return self.email
    

class LogRequest(models.Model):
    url = models.CharField(max_length=255)
    status_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    payload = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.method} {self.url} - {self.status_code} at {self.timestamp}"
    

class Transaction(models.Model):
    ASSET_CLASSES = [
        ('Equity', 'Equity'),
        ('Debt', 'Debt'),
        ('Alternate', 'Alternate'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    asset_class = models.CharField(max_length=20, choices=ASSET_CLASSES)
    date = models.DateField()
    units = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'product', 'date')

    def __str__(self):
        return f"{self.product} ({self.date}) - {self.user.email}"

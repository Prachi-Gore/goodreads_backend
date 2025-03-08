from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model;
from datetime import timedelta;
from django.core.validators import MinLengthValidator, RegexValidator
from django.conf import settings
from django.utils.timezone import now
import random
import uuid
import cloudinary

# Create your models here.

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True,null=False, blank=False)
    username = models.CharField(max_length=150, blank=False, null=False, unique=True)
    USERNAME_FIELD = 'email'  # Make email the default identifier

    REQUIRED_FIELDS = ['username']
    print("*** CustomUser model ")

    
    def __str__(self):
        return f'{self.email} {self.username}'
    
User=get_user_model()
class ForgotPasswordOtp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE) # could be multiple otp corresponding to single user
    otp= models.CharField(max_length=6,
        validators=[
            MinLengthValidator(6),  
            RegexValidator(r'^\d{6}$', 'OTP must be exactly 6 digits')  # Ensures only numbers
        ])
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)    

    def is_expired(self):
        return now() >self.created_at+timedelta(minutes=settings.OTP_EXPIRY_TIME)
    
    @staticmethod # same for all instance 
    def generate_otp():
        return random.randint(100000, 999999) # 6digits otp
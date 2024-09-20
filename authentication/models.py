from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
   
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email,password,**extra_fields
    ): 
        if not email:
            raise ValueError("The Email field must be set")

       
        user = self.model(
             email = self.normalize_email(email),**extra_fields
        
        )  
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email,password, **extra_fields):
       


         extra_fields.setdefault('is_staff', True),
         extra_fields.setdefault('is_superuser', True),
         user = self.create_user(
            email,
            password,
          
        **extra_fields
        ) 
      
        
         return user


class User(AbstractBaseUser, PermissionsMixin):
    class UserRole(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"
    phone_number = PhoneNumberField()
    email = models.EmailField(blank=False, unique=True)
    # device_id = models.CharField(max_length=100, blank=False)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=300, null=True,blank=True)
    middle_name = models.CharField(max_length=300, null=True,blank=True)
    last_name = models.CharField(max_length=300, null=True,blank=True)
    gender = models.ForeignKey('configuration.Gender', on_delete=models.CASCADE,blank=True,null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=30, choices=UserRole.choices)
    from configuration.models import Gender

    

from django.forms import ModelForm
from phonenumber_field.modelfields import PhoneNumberField
from .models import User
from django import forms

from django.forms import ModelForm

# from human_resource.models import Teacher, Student

class UserForm(ModelForm):
    class Meta:
        model = User
        phone_number = PhoneNumberField()
        fields = [
            "phone_number",
            "email",
            "password",
            "gender",
        ]
        widgets={
            "password":forms.PasswordInput(attrs={"placeholder":"Enter Password","class":"form-control"}),
            "email":forms.EmailInput(attrs={"placeholder":"Enter Email","class":"form-control"}),
            "first_name":forms.TextInput(attrs={"placeholder":"Enter First Name(Optional)","class":"form-control"}),
            "phone_number":forms.TextInput(attrs={"placeholder":"Enter Phone Number","class":"form-control"}),
            "gender":forms.Select(attrs={"style":"width:100%; height:35px;"}),
            
        }

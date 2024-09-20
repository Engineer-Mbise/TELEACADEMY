from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserChangeForm
from authentication.models import User
from .models import Gender
from .models import Payment
from .models import Progress
from .models import Level




class EditForm(UserChangeForm):
    password=None
    class Meta:
        model=User
      
        fields = [
            "first_name","middle_name","last_name","gender"
        ]
        widgets={
            "first_name":forms.TextInput(attrs={"placeholder":"Enter First Name","class":"form-control"}),
            "middle_name":forms.TextInput(attrs={"placeholder":"Enter Middle Name","class":"form-control"}),
            "last_name":forms.TextInput(attrs={"placeholder":"Enter Last Name","class":"form-control"}),
            "gender":forms.Select(attrs={"style":"width:100%; height:35px;"}),
            
        }

class GenderForm(ModelForm):
    class Meta:
        model = Gender
        fields = ["acronym", "description"]


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ["payment_status"]


class ProgressForm(ModelForm):
    class Meta:
        model = Progress
        # fields = ["progress_status", "status"]
        fields = "__all__"


class LevelForm(ModelForm):
    class Meta:
        model = Level
        fields = ["name"]

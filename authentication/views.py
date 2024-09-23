from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from phonenumber_field.phonenumber import PhoneNumber
# from human_resource.models import Teacher, Student
import pyotp

# Create your views here.
from .models import User
from configuration.models import Gender
from .forms import UserForm
from django.contrib import messages


def registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            try:
                validate_password(password)
            except ValidationError as e:
                for error in e:
                     messages.error(request, error,extra_tags='password_error')
                     
                return render(
                    request, 
                    "authentication/pages-register.html", 
                    {
                        "phone_number": form["phone_number"],
                        "email": form["email"],
                        "password": form["password"],
                        "gender": form["gender"],
                    }
                )
            user = form.save(commit=False)
            user_details=form.cleaned_data
            user_details["phone_number"] = str(user_details["phone_number"])
            request.session["gender_id"]=user_details["gender"].id
            del user_details["gender"]
            request.session["user_details"]=user_details
            gmail=user.email
            token=pyotp.random_base32()
            code=pyotp.TOTP(token,interval=300)
            email_message=code.now()
            message= f"""
                        Hi {gmail},

                        Welcome to  TELEACADEMY PLATFORM! We're excited to have you on board.

                        Please use the following code to verify your email address and complete your registration:

                        Verification Code: {email_message}

                        This code is valid for the next 5 minutes. If you did not request this email, please ignore it.

                        Thank you for choosing TELEACADEMY PLATFORM!

                        Best regards,
                        The TELEACADEMY PLATFORM Team

                        ---
                        This is an automated message, please do not reply.
                        """
            request.session["email_message"]=email_message
            request.session["gmail"]=gmail
            request.session["original_token"]=email_message
            request.session["generated_at"]=timezone.now().isoformat()
            send_mail("Email Verification",message,"teleacademy8@gmail.com",[gmail],fail_silently=False)
            # user.role = "STUDENT"
            # user.save()
            # is_teacher = form.cleaned_data.get("is_teacher", False)
            # is_student = form.cleaned_data.get("is_student", False)
            # messages.success(request, "Registered Successfully!")
            # return redirect("my_login_view")
            return redirect("token_verification")

        else:
            messages.error(request, "Registration failed.Also remember to enter a valid phone number",extra_tags="registration error message")
    else:
        form = UserForm()
    return render(
        request,
        "authentication/pages-register.html",
        {
            "phone_number": form["phone_number"],
            "email": form["email"],
            "password": form["password"],
            "gender": form["gender"],
            # "is_student": form["is_student"],
            # "is_teacher": form["is_student"],
            # "device_id": form["device_id"],
        },
    )

def token_verification(request):
    if request.method=="POST":
        token=request.POST.get("token")
        filled_at=timezone.now()
        generated_at = timezone.datetime.fromisoformat(request.session["generated_at"])
        
          # Retrieve and convert phone_number from string back to PhoneNumber
        user_details = request.session.get("user_details", {})
        phone_number_str = user_details.get("phone_number")
        if phone_number_str:
            phone_number = PhoneNumber.from_string(phone_number_str)
        if request.session.get("original_token")==token and (filled_at-generated_at)<=timedelta(seconds=300):
            user=User()
            user.password = make_password(request.session.get("user_details")["password"])
            user.email=request.session.get("user_details")["email"]
            user.gender=Gender.objects.get(id=request.session.get("gender_id"))
            user.phone_number=request.session.get("user_details")["phone_number"]
            user.role = "STUDENT"
            user.save()
            del request.session["gender_id"]
            del request.session["user_details"]
            del request.session["original_token"]
            del request.session["generated_at"]
            del request.session["gmail"]
            del request.session["email_message"]
            return redirect("my_login_view")
        elif not request.session.get("original_token")==token and (filled_at-generated_at)<=timedelta(seconds=300):
            messages.error(request,"Incorrect token,please enter the correct one!",extra_tags="token error")
            return redirect("token_verification")
        elif request.session.get("original_token")==token and not (filled_at-generated_at)<=timedelta(seconds=300):
            messages.error(request,"You was out of time,please fill this form again!",extra_tags="time error")
            return redirect("register")
        elif not request.session.get("original_token")==token and not (filled_at-generated_at)<=timedelta(seconds=300):
            messages.error(request,"You was out of time,please fill this form again!",extra_tags="time error")
            return redirect("register")
    
    return render(request,"authentication/token_verification.html")
        
def token_resending(request):
    
    
    message= f"""
                Hi teleacademyian,

                Welcome to  TELEACADEMY PLATFORM! We're excited to have you on board.

                Please use the following code to verify your email address and complete your registration:

                Verification Code: {request.session["email_message"]}

                This code is valid for the next 5 minutes. If you did not request this email, please ignore it.

                Thank you for choosing TELEACADEMY PLATFORM!

                Best regards,
                The TELEACADEMY PLATFORM Team

                ---
                This is an automated message, please do not reply.
                """
                
                        
    send_mail("Email Verification",message,"teleacademy8@gmail.com",[request.session["gmail"]],fail_silently=False)
    messages.info(request,"We sent you the previous token again,Please check your emails!",extra_tags="token resending info")
    return redirect("token_verification")
         
def home(request):
    return render(request, "authentication/home.html")


def my_login_view(request):
    if request.method == "POST":
        email=request.POST.get("username")
        password = request.POST.get("password")
        user=authenticate(email=email, password=password)

        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect("admin_dashboard")
            if user.role=='TEACHER':
                return redirect("teacher_dashboard")
            return redirect(reverse("configuration"))

        
        messages.error(request, "User with such details does not exist",extra_tags="login error")
            

    return render(
            request,
            "authentication/pages-login.html",
            
        )
    
    
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"Password was changed successfully,you may now log in with the new password!!",extra_tags="change_password_success")
            return redirect("my_login_view")
        else:
            messages.error(request,"Your old password must be correct, and the new password entries must match",extra_tags="password_change_error")
            
    else:
        form=PasswordChangeForm(request.user)
    return render(request,"configuration/change_password.html",{"form":form})



def logout_view(request):
    logout(request)
    return redirect("my_login_view")

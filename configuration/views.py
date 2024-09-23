from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EditForm
from django.contrib import messages
from authentication.models import User
from human_resource.models import Student
from .forms import (
    LevelForm,
    ProgressForm,
    PaymentForm,
    GenderForm,
)

# Create your views here.
from .models import Level, Progress, Payment, Gender
from courses.forms import LearningMaterialForm
from courses.models import LearningMaterial,Registered,Course,Quiz,Result,Response




@login_required
def configuration(request):
    available_quizes=Quiz.objects.count()
    taken_courses=Result.objects.filter(user=request.user).count()
    progress=round((taken_courses/1)*100)
    total_courses_registered=Registered.objects.filter(student=request.user).count()
    registered=Registered.objects.filter(student=request.user).values_list("course__id",flat=True)
    total_available_courses = Course.objects.all().count()
    return render(request, "configuration/base.html",{"total_courses_registered":total_courses_registered,"total_available_courses":total_available_courses,"progress":progress})




@login_required
def admin_dashboard(request):
    materials=LearningMaterial.objects.count()
    courses=Course.objects.count()
    instructors=User.objects.filter(role='TEACHER').count()
    students=User.objects.filter(role='STUDENT').count()
    quizes=Quiz.objects.count()
    
    return render(request,"configuration/admin.html",{"materials":materials,"instructors":instructors,"courses":courses,"students":students,"quizes":quizes})



@login_required
def teacher_dashboard(request):
    courses=Course.objects.filter(instructor=request.user)
    total_courses=courses.count()
    course_ids=courses.values_list('id',flat=True)
    quizes=Quiz.objects.filter(course__id__in=course_ids)
    total_quizes=quizes.count()
    return render(request,"configuration/teacher.html",{"total_courses":total_courses,"total_quizes":total_quizes})




@login_required
def my_quizes_results(request):
    courses=Course.objects.filter(instructor=request.user)
    course_ids=courses.values_list('id',flat=True)
    quizes=Quiz.objects.filter(course__id__in=course_ids)
    quiz_ids=quizes.values_list('id',flat=True)
    results=Result.objects.filter(quiz__id__in=quiz_ids)
    return render(request,"configuration/my_quizes_results.html",{"results":results})



@login_required
def student_responses(request,quiz_id,student_id):
    responses=Response.objects.filter(quiz__id=quiz_id,user__id=student_id)
    return render(request,"configuration/student_responses.html",{"responses":responses})
        
    
    


@login_required
def level(request):
    levels = Level.objects.all()
    if request.method == "POST":
        levelform = LevelForm(request.POST)
        if levelform.is_valid():
            levelform.save()
            messages.success(request, "A level was added successfully!!",extra_tags="level_message")

    else:
        levelform = LevelForm()
    return render(
        request,
        "configuration/level.html",
        {"name": levelform["name"], "levels": levels},
    )
    
    
    
def delete_level(request,pk):
    level_to_delete=Level.objects.get(id=pk)
    level_to_delete.delete()
    return redirect('level')



def delete_gender(request,pk):
    gender_to_delete=Gender.objects.get(id=pk)
    gender_to_delete.delete()
    return redirect('gender')



@login_required
def payment(request):
    payments = Payment.objects.all()
    if request.method == "POST":
        paymentform = PaymentForm(request.POST)
        if paymentform.is_valid():
            paymentform.save()
            messages.success(request, "Done!!!")
            return redirect("payment")

    else:
        paymentform = PaymentForm()
    return render(
        request,
        "configuration/payment.html",
        {
            "payment_status": paymentform["payment_status"],
            "payments": payments,
        },
    )



@login_required
def progress(request):
    progress = Progress.objects.all()
    if request.method == "POST":
        progressform = ProgressForm(request.POST)
        if progressform.is_valid():
            progressform.save()
            messages.success(request, "Done!!")
            return redirect("progress")

    else:
        progressform = ProgressForm()
    return render(
        request,
        "configuration/progress.html",
        {
            "progress_status": progressform["progress_status"],
            "progress": progress,
        },
    )



@login_required
def gender(request):
    genders = Gender.objects.all()
    if request.method == "POST":
        genderform = GenderForm(request.POST)
        if genderform.is_valid():
            genderform.save()
            messages.success(request, "A gender was added successfully",extra_tags="gender_added_message")
            return redirect("gender")

    else:
        genderform = GenderForm()

    return render(
        request,
        "configuration/gender.html",
        {
            "acronym": genderform["acronym"],
            "description": genderform["description"],
          
            "genders": genders,
        },
    )


@login_required
def my_profile(request):
    if request.method=="POST":
        form=EditForm(request.POST,instance=request.user)
      
        if form.is_valid():
            form.save()
            messages.info(request,"Profile updated successfully! Your changes have been saved",extra_tags="profile_edited_message")
            return redirect("profile")
    else:
        form=EditForm(instance=request.user)
    return render(request,"configuration/my_profile.html",{"form":form})
    



@login_required
def profile(request):
    details=User.objects.filter(email=request.user)
    return render(
        request,
        "configuration/profile.html",
        {
            "details": details,
        },
    )



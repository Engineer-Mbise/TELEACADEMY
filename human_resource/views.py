from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from courses.models import Course
from .models import Message

def discussion_courses(request):
    courses=Course.objects.all()
    return render(request,"human_resource/discussions.html",{"courses":courses})


def messages(request,pk): 
    course=Course.objects.get(id=pk)
    sender=request.user
    messages=Message.objects.filter(course__id=pk)
    return render(request,"human_resource/messages.html",{"messages":messages,"course":course,"sender":sender})
    
    
    




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
from .forms import LearningMaterialForm,CourseForm,QuizForm,QuestionForm
from .models import LearningMaterial,Course,Registered,Result,Question,Response,Quiz
from django.core.paginator import Paginator
from human_resource.models import Student
from django.db.models import Sum,Avg




@login_required
def add_course(request):
    courses = Course.objects.filter(instructor=request.user)
    if request.method == "POST":
        courseform = CourseForm(request.POST)
        if courseform.is_valid():
            instance=courseform.save(commit=False)
            instance.instructor=request.user
            instance.save()
            messages.success(request,"Course added successfully!",extra_tags="course added")
    else:
        courseform = CourseForm()

    return render(
        request,
        "courses.html",
        {
            "courses": courses,
            "name": courseform["name"],
            "description": courseform["description"],
            "level": courseform["level"],
            
        },
    )
    
 
 
 
    
@login_required   
def add_quiz(request):
      instructor=request.user
      quizes = Quiz.objects.filter(course__instructor=instructor)
      courses=Course.objects.filter(instructor=request.user)
      if request.method == "POST":
        Quizform = QuizForm(request.POST)
        if Quizform.is_valid():
            instance=Quizform.save(commit=False)
            course=instance.course
            my_courses=Registered.objects.filter(course=course)
            instance.save()
            messages.success(request,"Quiz added successfully!",extra_tags="quiz added")
            for my_course in my_courses:
               student=my_course.student
               send_mail("New Quiz","A new quiz has been added to the course "+course.name+" that you are enrolled in.","teleacademy8@gmail.com",[student],fail_silently=False)     
     
      else:
        Quizform = QuizForm()
        Quizform.fields['course'].queryset=courses

      return render(
        request,
        "assesments.html",
        {
            "quizes": quizes,
            "title": Quizform["title"],
            "description": Quizform["description"],
            "course": Quizform["course"],
            
        },
    )
    


def add_question(request,pk):
    questions = Question.objects.filter(quiz__id=pk)
    quizes=Quiz.objects.filter(course__instructor=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Question added successfully!",extra_tags="question added")
       
          

    else:
        form = QuestionForm()
        form.fields['quiz'].queryset=quizes
    return render(
        request,
        "questions.html",
        {
            "questions": questions,
            "quiz": form["quiz"],
            "statement": form["statement"],
            "option1": form["option1"],
            "option2": form["option2"],
            "option3": form["option3"],
            "option4": form["option4"],
            "correct_answer": form["correct_answer"],
            "time_to_answer_in_seconds": form["time_to_answer_in_seconds"],
                
          
        },
    )

 
    
    
    

@login_required
def all_courses(request):
    registered=Registered.objects.filter(student=request.user).values_list("course__id",flat=True)
    all_courses = Course.objects.exclude(id__in=registered)
    p=Paginator(all_courses,10)
    page_number=request.GET.get("page")
    all_courses=p.get_page(page_number)
    return render(
        request,
        "all_courses.html",
        {"all_courses":all_courses},
      
    )  

@login_required 
def learningmaterials(request, pk):
    learningMaterials = LearningMaterial.objects.filter(course__id=pk)
    courses=Course.objects.filter(instructor=request.user)

    if request.method == "POST":
        form = LearningMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Learning material added successfully!",extra_tags="learning material added")
            return redirect("course")
          

    else:
        form = LearningMaterialForm()
        form.fields['course'].queryset=courses
    return render(
        request,
        "learning_materials.html",
        {
            "learningMaterials": learningMaterials,
            "course": form["course"],
            "video": form["video"],
            "audio": form["audio"],
            "notes": form["notes"],
          
        },
    )


@login_required
def selected_courses(request,pk):
    courses = Course.objects.get(id=pk)
    if not Registered.objects.filter(course=courses,student=request.user).exists():
        register, create = Registered.objects.get_or_create(
            course=courses,
            student=request.user,
        )
        messages.success(request,"Course selected successfully!",extra_tags="course selected")
        return redirect("registered")
        
            
            
        
    else:
         
            return redirect("all_courses")
    

@login_required
def render_selected(request):
    registered = Registered.objects.filter(student=request.user)
    p=Paginator(registered,10)
    page_number=request.GET.get("page")
    registered=p.get_page(page_number)
    return render(request, "selected_courses.html", {"registered": registered})


@login_required
def cancel_course_selection(request, pk):
    deleted = Registered.objects.filter(id=pk)
    deleted.delete()
    messages.success(request,"Course selection canceled successfully!!",extra_tags="cancel course")
    return redirect("registered")

@login_required
def delete_course(request,pk):
    course_to_delete=Course.objects.filter(id=pk)
    course_to_delete.delete()
    messages.success(request,"Course deleted successfully!",extra_tags="course deleted")
    return redirect("course")

   
@login_required
def delete_learning_material(request,pk):
    material_to_delete=LearningMaterial.objects.get(id=pk)
    course_id=material_to_delete.course.id
    material_to_delete.delete()
    messages.success(request,"Learning material deleted successfully!",extra_tags="learning material deleted")
    return redirect("learningmaterials",pk=course_id)

    
@login_required
def delete_quiz(request,pk):
    quiz_to_delete=Quiz.objects.get(id=pk)
    quiz_to_delete.delete()
    messages.success(request,"Quiz deleted successfully!",extra_tags="quiz deleted")
    return redirect("add_quiz")
    
  

@login_required
def delete_question(request,pk):
    question_to_delete=Question.objects.get(id=pk)
    quiz_id=question_to_delete.quiz.id
    question_to_delete.delete()
    messages.success(request,"Question deleted successfully!",extra_tags="question deleted")
    return redirect("add_question",pk=quiz_id)




@login_required
def materials(request, pk):
    materials = LearningMaterial.objects.filter(course__id=pk)
    return render(request, "materials.html", {"materials": materials})




@login_required
def search_all_courses(request):
    searched_data=request.POST.get("query")
    data=Course.objects.filter(name__icontains=searched_data)
    zero_results=False
    if not data.exists():
        zero_results=True
    return render(request,"search_all_courses.html",{"data":data,"zero_results":zero_results})




@login_required
def search_courses(request):
    searched_course=request.POST.get("query")
    searched_courses=Course.objects.filter(name__icontains=searched_course)
    zero_results=False
    if not searched_courses.exists():
        zero_results=True
    return render(request,"search_courses.html",{"searched_courses":searched_courses,"zero_results":zero_results})



@login_required
def search_selected_courses(request):
    searched_selected_course=request.POST.get("query")
    searched_selected_courses=Registered.objects.filter(course__name__icontains=searched_selected_course,student=request.user)
    zero_results=False
    if not searched_selected_courses.exists():
        zero_results=True 
    return render(request,"search_selected_courses.html",{"searched_selected_courses":searched_selected_courses,"zero_results":zero_results})





@login_required
def take_quiz(request,quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    result,created=Result.objects.get_or_create(quiz_id=quiz_id,user=request.user)
    taken=result.taken
    time=Question.objects.filter(quiz_id=quiz_id).aggregate(Sum('time_to_answer_in_seconds'))['time_to_answer_in_seconds__sum']

    if request.method == 'POST':
        questions = Question.objects.filter(quiz=quiz)
        number_of_questions=questions.count()
        correct_answers=0
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option == question.correct_answer:
               correct_answers +=1 
        score=round((correct_answers/number_of_questions)*100)
        result, created = Result.objects.get_or_create(quiz=quiz, user=request.user)
        response,created=Response.objects.get_or_create(quiz=quiz,user=request.user,response=selected_option,question=question)
        response.save()
        result.score = score
        result.save()
        return render(request,"quiz_results.html",{'questions': questions,'result': result,"response":response})
    else:
        result.taken = True
        result.save()
        
        questions = Question.objects.filter(quiz=quiz).order_by('?')
        
   
        
    return render(request, 'take_quiz.html', {'questions': questions,"quiz":quiz,'result': result,'time':time,'taken':taken})



@login_required
def quiz_answers(request,quiz_id):
    
    questions=Question.objects.filter(quiz_id=quiz_id)
   
      
    return render(request,"answers.html",{'questions':questions})
    
    
    


@login_required
def list_of_quizes(request):
    attempted=Result.objects.filter(user=request.user).values_list('quiz__id',flat=True)
    quizes=Quiz.objects.exclude(id__in=attempted)
    return render(request,'quizes.html',{"quizes":quizes})


@login_required
def quiz_results(request):
    results=Result.objects.filter(user=request.user)
    return render(request,"my_results.html",{"results":results})



@login_required
def quiz_instructions(request,pk):
    quiz=Quiz.objects.get(id=pk)
    time=Question.objects.filter(quiz_id=pk).aggregate(Sum('time_to_answer_in_seconds'))['time_to_answer_in_seconds__sum']
    
    return render(request,"instructions.html",{"quiz":quiz,"time":time})





@login_required
def retake_quiz(request,quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    result,created=Result.objects.get_or_create(quiz_id=quiz_id,user=request.user)
    retaken=result.retaken
    time=Question.objects.filter(quiz_id=quiz_id).aggregate(Sum('time_to_answer_in_seconds'))['time_to_answer_in_seconds__sum']

    if request.method == 'POST':
        questions = Question.objects.filter(quiz=quiz)
        number_of_questions=questions.count()
        correct_answers=0
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option == question.correct_answer:
               correct_answers +=1 
        score=round((correct_answers/number_of_questions)*100)
        result, created = Result.objects.get_or_create(quiz=quiz, user=request.user)
        response,created=Response.objects.get_or_create(quiz=quiz,user=request.user,response=selected_option,question=question)
        response.save()
        result.score = score
        result.save()
        return render(request,"quiz_results.html",{'questions': questions,'result': result,"response":response})
   
    else:
        result.retaken = True
        result.save()
        questions = Question.objects.filter(quiz=quiz).order_by('?')
        
   
        
    return render(request, 'take_quiz.html', {'questions': questions,"quiz":quiz,'result': result,'time':time,"retaken":retaken})







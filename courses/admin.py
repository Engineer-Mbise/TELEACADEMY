from django.contrib import admin
from .models import LearningMaterial,Course,Registered,Question,Result,Response,Quiz


class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ["course", "video", "notes"]


class QuizAdmin(admin.ModelAdmin):
    list_display=["title","description","course"]


class CourseAdmin(admin.ModelAdmin):
    list_display = ["description","name","level","instructor"]
    
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["quiz","statement","option1","option2","option3","option4","correct_answer","time_to_answer_in_seconds"]
    

class ResultAdmin(admin.ModelAdmin):
    list_display = ["user","quiz","score","retaken"]
    

class ResponseAdmin(admin.ModelAdmin):
    list_display=['quiz','user','question','response']


@admin.register(Registered)
class SelectedAdmin(admin.ModelAdmin):
    list_display = [
        "course",
        "student",
       
    ]

admin.site.register(LearningMaterial, LearningMaterialAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Response,ResponseAdmin)
admin.site.register(Quiz,QuizAdmin)



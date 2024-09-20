from django.forms import ModelForm
from .models import LearningMaterial,Course,Question,Quiz
from django import forms
from .models import Registered

class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude=["instructor"]
        fields =["name","description","level"]
        


class LearningMaterialForm(ModelForm):
    class Meta:
        model = LearningMaterial
        fields = ["course", "video","audio","notes"]
        
        
class QuizForm(ModelForm):
    class Meta:
        model=Quiz
        fields="__all__"
        

class QuestionForm(ModelForm):
    class Meta:
        model=Question
        fields="__all__"
        


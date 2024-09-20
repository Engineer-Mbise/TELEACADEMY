from configuration.models import Level
from configuration.models import Payment
from configuration.models import Progress
from authentication.models import User


# Create your models here.
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import FileExtensionValidator
audioExt_validator=FileExtensionValidator(["MP3","WAV","FLAC","AAC"])
videoExt_validator=FileExtensionValidator(["MP4","AVI","MKV","FLV","WMV","MOV","WEBM"])
notesExt_validator=FileExtensionValidator(["PDF", "DOC", "DOCX", "ODT", "RTF", "TXT", "HTML", "XLS", "XLSX", "ODS", "PPT", "PPTX", "EPUB", "MOBI", "CSV", "JSON", "XML", "PS", "TEX", "MD"])


class Course(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.CharField(max_length=300)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    instructor=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        

class LearningMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video = models.FileField(upload_to="videos/", validators=[videoExt_validator])
    audio=models.FileField(upload_to='audio/',validators=[audioExt_validator])
    notes = models.FileField(upload_to="notes/", validators=[notesExt_validator])
    
    class Meta:
        verbose_name = "LearningMaterial"
        verbose_name_plural = "LearningMaterials"
    


    
class Registered(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey("authentication.User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Registered Course"
        verbose_name_plural = "Registered Courses"
        
        
        
        
class Quiz(models.Model):
    title=models.CharField(max_length=250)
    description=models.CharField(max_length=250)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name='Quiz'
        verbose_name_plural='Quizes'
    

class Question(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    statement=models.TextField()
    option1=models.CharField(max_length=250)
    option2=models.CharField(max_length=250)
    option3=models.CharField(max_length=250)
    option4=models.CharField(max_length=250)
    correct_answer=models.CharField(max_length=10,choices=[('option1','option1'),('option2','option2'),('option3','option3'),('option4','option4')])
    time_to_answer_in_seconds=models.IntegerField(default=0)
    def __str__(self):
        return self.statement
    
    class Meta:
        verbose_name='Question'
        verbose_name_plural='Questions'



class Result(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    score=models.PositiveIntegerField(default=0)
    taken=models.BooleanField(default=0)
    retaken=models.BooleanField(default=0)
    
    class Meta:
        verbose_name='Result'
        verbose_name_plural='Results'
    
class Response(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    response=models.CharField(max_length=250,null=True,blank=True)
    
    class Meta:
        verbose_name='Response'
        verbose_name_plural='Responses'
 
    
    

    

    
    

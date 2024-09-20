from django.db import models
from configuration.models import Gender
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import Signal, receiver
from configuration.models import Level,Gender
from django_ckeditor_5.fields import CKEditor5Field

from authentication.models import User
from courses.models import Course

# from django.contrib.auth.models import User

# Create your models here.




class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(max_length=300)
    middle_name = models.CharField(max_length=300, blank=True)
    last_name = models.CharField(max_length=300)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email}"
    
    class Meta:
        verbose_name="Student"
        verbose_name_plural="Students"
        
        


class Teacher(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(max_length=300)
    middle_name = models.CharField(max_length=300, blank=True)
    last_name = models.CharField(max_length=300)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email}"
    
    class Meta:
        verbose_name="Teacher"
        verbose_name_plural="Teachers"
    
    
class Message(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    message=CKEditor5Field(null=True,blank=True)
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name="Message"
        verbose_name_plural="Messages"
        
        


# # class UserParticulars(models.Model):
# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #     first_name = models.CharField(max_length=300, null=True,verbose_name="First Name:")
# #     middle_name = models.CharField(max_length=300, null=True)
# #     last_name = models.CharField(max_length=300, null=True)
# #     gender = models.ForeignKey(Gender, on_delete=models.CASCADE,blank=False)
# #     def __str__(self):
# #         return f"{self.user.email}-{self.first_name}-{self.middle_name}-{self.last_name}-{self.gender.acronym}_{self.gender.description}"


# # @receiver(post_save, sender=User)
# # def create_teacher_profile(sender, created, instance, **kwargs):
# #     if created:
# #         UserParticulars.objects.create(user=instance)

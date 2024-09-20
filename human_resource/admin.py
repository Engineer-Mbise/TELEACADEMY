from django.contrib import admin

# Register your models here.
from .models import Student,Message
# # from .models import Teacher
# # from .models import UserParticulars


class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "level",
        "first_name",
        "middle_name",
        "last_name",
        "gender",
    ]
    

class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "course",
        "message",
        "sender",
        "created_at",
       
    ]


# # class TeacherAdmin(admin.ModelAdmin):
# #     list_display = [
# #         "user",
# #         "first_name",
# #         "middle_name",
# #         "last_name",
# #         "course",
# #         "gender",
# #     ]


# class UserParticularsAdmin(admin.ModelAdmin):
#     list_display = [
#         "user",
#         "first_name",
#         "middle_name",
#         "last_name",
#         "gender",
#     ]


# admin.site.register(UserParticulars, UserParticularsAdmin)
# # admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Message, MessageAdmin)

# """
# admin.site.register(UserParticulars)
# admin.site.register(Teacher)
# admin.site.register(Student)
# """

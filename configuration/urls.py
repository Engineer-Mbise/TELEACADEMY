from django.urls import path
from . import views

urlpatterns = [
    path("dashboard", views.configuration, name="configuration"),
    path("admin_dashboard", views.admin_dashboard, name="admin_dashboard"),
    path("my_quizes_results",views.my_quizes_results,name="my_quizes_results"),
    path("student_responses/<int:quiz_id>/<int:student_id>/",views.student_responses,name="student_responses"),
    path("teacher_dashboard", views.teacher_dashboard, name="teacher_dashboard"),
    path("gender", views.gender, name="gender"),
    path("progress/<int:pk>/", views.progress, name="progress"),
    path("level", views.level, name="level"),
    path("payment", views.payment, name="payment"),
    path("update_profile",views.my_profile,name="my_profile"),
    path("my_profile", views.profile, name="profile"),
    path("delete_level/<int:pk>/",views.delete_level,name="delete_level"),
    path("delete_gender/<int:pk>/",views.delete_gender,name="delete_gender"),
  
]

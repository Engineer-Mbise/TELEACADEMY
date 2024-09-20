from django.urls import path
from . import views


urlpatterns = [
    path("discussions/",views.discussion_courses,name="discussion_courses"),
    path("messages/<int:pk>/",views.messages,name="messages"),
]

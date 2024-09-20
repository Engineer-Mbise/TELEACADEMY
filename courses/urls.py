from django.urls import path
from . import views
name="courses"
urlpatterns = [
    path("learningmaterial/<int:pk>/", views.learningmaterials, name="learningmaterials"),
    path("course/",views.add_course,name="course"),
    path("selected_courses/<int:pk>/",views.selected_courses,name="selected_courses"),
    path("cancel_course_selection/<int:pk>/",views.cancel_course_selection,name="cancel_course_selection"),
    path("render_selected/",views.render_selected,name="registered"),
    path("all_courses/",views.all_courses,name="all_courses"),
    path("materials/<int:pk>/",views.materials,name="materials"),
    path("search_all_courses/",views.search_all_courses,name="search_all_courses"),
    path("search_courses/",views.search_courses,name="search_courses"),
    path("search_selected_courses/",views.search_selected_courses,name="search_selected_courses"),
    path('quizes',views.list_of_quizes,name='quizes'),
    path("take_quiz/<int:quiz_id>/",views.take_quiz,name="take_quiz"),
    path("retake_quiz/<int:quiz_id>/",views.retake_quiz,name="retake_quiz"),
    path("quiz_results",views.quiz_results,name="quiz_results"),
    path("quiz_answers/<int:quiz_id>",views.quiz_answers,name="quiz_answers"),
    path("add_quiz",views.add_quiz,name="add_quiz"),
    path("add_question/<int:pk>",views.add_question,name="add_question"),
    path("delete_course/<int:pk>",views.delete_course,name="delete_course"),
    path("delete_learning_material/<int:pk>",views.delete_learning_material,name="delete_learning_material"),
    path("delete_quiz/<int:pk>",views.delete_quiz,name="delete_quiz"),
    path("delete_question/<int:pk>",views.delete_question,name="delete_question"),
    path("quiz_instructions/<int:pk>",views.quiz_instructions,name="quiz_instructions"),
    
     
]

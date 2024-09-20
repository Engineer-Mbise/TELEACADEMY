from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

# app_name = "Authentication"
urlpatterns = [
    path("", views.my_login_view, name="my_login_view"),
    path("register", views.registration, name="register"),
    path("home", views.home, name="home"),
    path("logout", views.logout_view, name="logout"),
    path("changing_password", views.change_password, name="change_password"),
    path("token_verification/",views.token_verification,name="token_verification"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html'),name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'),name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'),name="password_reset_confirm"),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),name="password_reset_complete"),
    path("token_resending/",views.token_resending,name="token_resending"),
    
]

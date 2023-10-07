# Django Imports
from django.urls import path, include

# Local Imports
from . import views

app_name = 'users_app'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('verification-user/<pk>/', views.CodeVerificationView.as_view(), name='verification-user'),
]
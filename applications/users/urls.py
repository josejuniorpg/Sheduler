# Django Imports
from django.urls import path, include
from django.contrib.auth.views import LogoutView

# Local Imports
from . import views

app_name = 'users_app'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('verification-user/<pk>/', views.CodeVerificationView.as_view(), name='verification-user'),
    path('send-again-email/<pk>/', views.send_again_email_view, name='send-again-email'),
]
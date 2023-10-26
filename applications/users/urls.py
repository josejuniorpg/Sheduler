# Django Imports
from django.urls import path, include, reverse_lazy
import django.contrib.auth.views as auth_views

# Local Imports
from . import views

app_name = 'users_app'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/update', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('verification-user/<pk>/', views.CodeVerificationView.as_view(), name='verification-user'),
    path('send-again-email/<pk>/', views.send_again_email_view, name='send-again-email'),

    #  Password Reset
    path('password-reset/',views.UserPasswordResetView.as_view(template_name='users/password_reset.html', html_email_template_name='users/password_reset_email.html'),
         name='password-reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/',views.UserPasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', success_url=reverse_lazy('users_app:password-reset-complete')),
         name='password-reset-confirm'),
    path('password-reset-complete/',auth_views. PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password-reset-complete'),

    # Change Password
    path('password-change/', views.UserPasswordChangeView.as_view(success_url=reverse_lazy('users_app:password-change-done')),
         name='password-change'),
    path('password-change/done', auth_views.PasswordChangeDoneView.as_view(template_name = 'users/password_change_done.html'), name='password-change-done')
]
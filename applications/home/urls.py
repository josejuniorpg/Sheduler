# Django Imports
from django.urls import path, include

# Local Imports
from . import views

app_name = 'home_app'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('change-language/<str:new_language>/', views.ChangeLanguageView.as_view(), name='change-language'),
    path('terms/', views.TermsAndConditionsView.as_view(), name='terms-conditions')
]
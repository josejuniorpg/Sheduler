# Django Imports
from django.urls import path, reverse_lazy
from . import views


# Local Imports
from . import views

app_name = 'shifts_app'

urlpatterns = [
    path('create/', views.HomePageView.as_view(), name='create'),
]
# Django Imports
from django.urls import path, reverse_lazy

# Local Imports
from . import views

app_name = 'shifts_app'

urlpatterns = [
    path('create-shift/', views.ShiftCreateView.as_view(), name='create_shifts'),
    path('list-shift/', views.ShiftListView.as_view(), name='create_shifts'),
]
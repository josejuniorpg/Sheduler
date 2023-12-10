# Django Imports
from django.urls import path, reverse_lazy

# Local Imports
from . import views

app_name = 'shifts_app'

urlpatterns = [
    path('create-shift/', views.ShiftCreateView.as_view(), name='create-shifts'),
    path('list-shift/', views.ShiftListView.as_view(), name='list-shifts'),
    path('update-shift/', views.ShiftListView.as_view(), name='update-shifts'), #todo finish this template.
    path('filter-shift/', views.FilterListView.as_view(), name='filter-shifts'),
]
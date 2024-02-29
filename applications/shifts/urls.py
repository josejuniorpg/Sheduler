# Django Imports
from django.urls import path, reverse_lazy

# Local Imports
from . import views

app_name = 'shifts_app'

urlpatterns = [
    path('create-shift/', views.ShiftCreateView.as_view(), name='create-shifts'),
    path('list-shift/', views.ShiftListView.as_view(), name='list-shifts'),
    path('list-daily/', views.ShiftDailyListView.as_view(), name='list-daily'),
    path('update-shift/<pk>', views.ShiftDetailsView.as_view(), name='update-shifts'),
    path('filter-shift/', views.FilterListView.as_view(), name='filter-shifts'),  # todo finish the Filters Logic
    path('list-user/', views.ShiftListUsers.as_view(), name='list-users'),
]
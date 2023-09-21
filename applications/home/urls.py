# Django Imports
from django.urls import path, include

# Local Imports
from . import views

app_name = 'home_app'

urlpatterns = [
    # path('', views.NewDepartamentoView.as_view(), name='new-departamento'),
    path('pruebas/', views.HomePageView.as_view(), name='home'),
]
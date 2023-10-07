# Django imports
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView, TemplateView


# Local imports

# Create your views here.

class UserRegisterView(TemplateView):
    template_name = 'users/register.html'
    # form_class = UserRegisterForm
    success_url = '/'
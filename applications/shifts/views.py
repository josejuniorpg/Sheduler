# Django imports
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from applications.shifts.forms import ShiftForm
from applications.shifts.models import Shift


# Create your views here.

class ShiftCreateView(CreateView):
    template_name = "shifts/create_shifts.html"
    model = Shift
    form_class = ShiftForm
    success_url = reverse_lazy('home_app:home')



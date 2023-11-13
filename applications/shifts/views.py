# Django imports
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from applications.shifts.forms import ShiftForm
from applications.shifts.models import Shift


# Create your views here.

class ShiftCreateView(CreateView):
    template_name = "shifts/create_shifts.html"
    model = Shift
    form_class = ShiftForm
    success_url = reverse_lazy('home_app:home')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            if 'save' in request.POST:
                return redirect(reverse_lazy('home_app:home'))
            elif 'save_and_add_another' in request.POST:
                return redirect(reverse_lazy('shifts_app:create_shifts'))
        # If the form is invalid, it renders the template with errors.
        return render(request, self.template_name, {'form': form})



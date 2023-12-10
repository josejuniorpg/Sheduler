# Django imports
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from applications.shifts.forms import CreateShiftForm
from applications.shifts.models import Shift


# Create your views here.

class ShiftCreateView(CreateView):
    template_name = "shifts/create_shifts.html"
    model = Shift
    form_class = CreateShiftForm
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
                return redirect(reverse_lazy('shifts_app:create-shifts'))
        # If the form is invalid, it renders the template with errors.
        return render(request, self.template_name, {'form': form})


class ShiftListView(ListView):
    template_name = "shifts/list_shifts.html"
    # model = Shift
    context_object_name = 'shifts'
    paginate_by = 10

    def get_queryset(self):
        kwargs = self.request.GET.get('search-shifts', '')
        print(kwargs)
        queryset = Shift.objects.filter(
            Q(user__first_name__icontains=kwargs) |
            Q(user__last_name__icontains=kwargs))
        return queryset


class FilterListView(ListView):
    template_name = "shifts/filter_shifts.html"
    # model = Shift
    context_object_name = 'filters'
    paginate_by = 10

    def get_queryset(self):
        kwargs = self.request.GET.get('search-shifts', '')
        print(kwargs)
        queryset = Shift.objects.filter(
            Q(user__first_name__icontains=kwargs) |
            Q(user__last_name__icontains=kwargs))
        return queryset


class ShiftDetailsView(UpdateView):
    template_name = "shifts/update_shifts.html"

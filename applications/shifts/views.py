# Django imports
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from applications.shifts.forms import CreateShiftForm, FiltersShiftForm, UpdateShiftForm
from applications.shifts.models import Shift, ShiftCategory
from applications.users.models import User


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
        queryset = Shift.objects.filter(
            Q(user__first_name__icontains=kwargs) |
            Q(user__last_name__icontains=kwargs))
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['search'] = self.request.GET.get('search-shifts', '')
        context = super().get_context_data(**kwargs)
        return context


class FilterListView(ListView):  # Maybe Change the name of this view
    template_name = "shifts/filter_shifts.html"
    context_object_name = 'filters'
    paginate_by = 10
    form_class = FiltersShiftForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class ShiftDetailsView(UpdateView):
    model = Shift
    template_name = "shifts/update_shifts.html"
    success_url = reverse_lazy('shifts_app:list-shifts')
    form_class = UpdateShiftForm
    context_object_name = 'shift'


class ShiftListUsers(ListView):
    template_name = "shifts/list_users.html"
    context_object_name = 'users'
    paginate_by = 3

    def get_queryset(self):
        return User.objects.values('email', 'first_name', 'last_name', 'profile_image', 'phone_number', 'status')


class ShiftDailyListView(ListView):
    template_name = "shifts/list_shifts.html"
    # model = Shift
    context_object_name = 'shifts'
    paginate_by = 10

    def get_queryset(self):
        kwargs = self.request.GET.get('search-shifts', '')
        queryset = Shift.objects.filter(
            Q(user__first_name__icontains=kwargs) |
            Q(user__last_name__icontains=kwargs))
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['search'] = self.request.GET.get('search-shifts', '')
        context = super().get_context_data(**kwargs)
        return context


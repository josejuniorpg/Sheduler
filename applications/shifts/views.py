# Django imports
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from applications.shifts.forms import CreateShiftForm, FiltersShiftForm
from applications.shifts.models import Shift, ShiftCategory


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

    def post(self, request, *args, **kwargs):
        status = True if request.POST.get('status') == 'on' else False
        is_temporal = True if request.POST.get('is_temporal') == 'on' else False

        filters = ("Status: " + str(status) + " ,Temporal: " + str(is_temporal) + " ,Categories: "
                   + str(list(ShiftCategory.objects.filter(id__in=request.POST.getlist('shift_category'))
                        .values_list('name', flat=True))))

        min_duration = request.POST.get('min_duration') if request.POST.get('min_duration') else 0
        max_duration = request.POST.get('max_duration') if request.POST.get('max_duration') else 100

        queryset = Shift.objects.filter(
            Q(shift_category__in=request.POST.getlist('shift_category'),
              status=status, is_temporal=is_temporal, duration__range=(min_duration, max_duration)))
        if not queryset:
            queryset = Shift.objects.filter(
                Q(status=status, is_temporal=is_temporal)
                & Q(duration__range=(min_duration, max_duration)))
        return render(request, self.template_name, {'shifts': queryset, 'filters': filters})
        # Because Filter don't existed before, won't save when I use method Get


class FilterListView(ListView):
    template_name = "shifts/filter_shifts.html"
    context_object_name = 'filters'
    paginate_by = 10
    form_class = FiltersShiftForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class ShiftDetailsView(UpdateView):
    template_name = "shifts/update_shifts.html"

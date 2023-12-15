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
    paginate_by = 1

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

        # todo Hacer esto una funcion, para asi reutilizarlo con la funcion de cookie.
        queryset = Shift.objects.filter(
            Q(shift_category__in=request.POST.getlist('shift_category'),
              status=status, is_temporal=is_temporal, duration__range=(min_duration, max_duration)))
        if not queryset:
            queryset = Shift.objects.filter(
                Q(status=status, is_temporal=is_temporal)
                & Q(duration__range=(min_duration, max_duration)))

        # Pagination
        def paginate_elements(page_size, current_page, elements_list):
            page_size = page_size
            current_page = current_page
            incomplete_page = None
            has_previous = True
            has_next = True
            total_pages = 0
            elements_list = elements_list
            total_elements = elements_list.count()
            elements_in_page = []

            # To obtain the incomplete page, if any, and the total number of pages.
            complete_pages, remainder_elements = divmod(total_elements, page_size)
            total_pages = complete_pages
            if remainder_elements > 0 or complete_pages <= 0:
                incomplete_page = complete_pages + 1
                total_pages = incomplete_page

            # Verification against extra pages.
            if incomplete_page:
                if current_page > incomplete_page:
                    raise Exception('The number of pages exceeds the number of available elements.')
            else:
                if current_page > complete_pages:
                    raise Exception('The number of pages exceeds the number of available elements.')

            # Element on which the current page is iterated.
            if current_page != 1:
                begin_element = page_size * (current_page - 1)  # Este es el numero de entrada.
            else:
                begin_element = 0

            # Create the elements of the page
            if current_page == incomplete_page:
                begin_element_remainder = page_size * complete_pages
                page_size = remainder_elements
                for i in range(page_size):
                    actual_element = begin_element_remainder + i
                    elements_in_page.append(elements_list[actual_element])
            else:
                for i in range(page_size):
                    actual_element = begin_element + i
                    elements_in_page.append(elements_list[actual_element])

            if current_page <= 1:
                has_previous = False
            if incomplete_page:
                if current_page >= incomplete_page:
                    has_next = False
            else:
                if current_page >= complete_pages:
                    has_next = False

            return {
                'current_page': current_page,
                'total_pages': total_pages,
                'has_previous': has_previous,
                'has_next': has_next,
                'elements_in_page': elements_in_page,
                'total_elements': total_elements,
            }

        # Todo create the cookie for the filters.
        resultado = paginate_elements(1, 3, queryset)  # La del Post debe estar siempre en`1.

        return render(request, self.template_name,
                      {'shifts': queryset, 'filters': filters, 'mi_diccionario': resultado})


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

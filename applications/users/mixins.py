# Django Imports
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect

class AnonymousRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home_app:home'))

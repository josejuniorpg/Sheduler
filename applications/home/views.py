# Django Imports
from django.shortcuts import render
from django.views.generic import (TemplateView)
from django.utils.translation import gettext as _

class HomePageView(TemplateView):
    template_name = "home/index.html"
    output = _("Welcome | Home Page")
    extra_context = {'title':output}
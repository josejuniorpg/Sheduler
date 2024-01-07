# Django Imports
from django.shortcuts import render
from django.views.generic import (TemplateView)
from django.utils.translation import gettext as _
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.utils import translation
from django.views import View

# Local Imports
from scheduler.settings.base import LANGUAGE_COOKIE_NAME
from scheduler import settings


class HomePageView(TemplateView):
    template_name = "home/index.html"


class ChangeLanguageView(View):
    def get(self, request, new_language):
        if new_language in [lang[0] for lang in settings.base.LANGUAGES]:
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home_app:home')))
            response.set_cookie(LANGUAGE_COOKIE_NAME, new_language)
            translation.activate(new_language)
            return response
        else:
            return HttpResponseNotFound("Language not found")


class TermsAndConditionsView(TemplateView):
    template_name = "home/terms-conditions.html"

# Django imports
from django.contrib import admin

# Local imports
from .models import Shift, Category

# Register your models here.
admin.site.register(Shift)
admin.site.register(Category)

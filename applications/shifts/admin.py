# Django imports
from django.contrib import admin

# Local imports
from .models import Shift, ShiftCategory, Scheduler, DailyScheduler, Assistance, Missing, MissingCategory

# Register your models here.
admin.site.register(Shift)
admin.site.register(ShiftCategory)
admin.site.register(Scheduler)
admin.site.register(DailyScheduler)
admin.site.register(Assistance)
admin.site.register(Missing)
admin.site.register(MissingCategory)


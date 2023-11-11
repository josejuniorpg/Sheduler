# Django imports
from django.contrib import admin

# Local imports
from .models import (Shift, ShiftCategory, Scheduler, ShiftDaily, Assistance, Missing, MissingCategory,
                     JustificationCategory, Justification)

# Register your models here.
admin.site.register(Shift)
admin.site.register(ShiftCategory)
admin.site.register(Scheduler)
admin.site.register(ShiftDaily)
admin.site.register(Assistance)
admin.site.register(Missing)
admin.site.register(MissingCategory)
admin.site.register(JustificationCategory)
admin.site.register(Justification)

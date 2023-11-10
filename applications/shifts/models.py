# Django imports
from django.db import models

# Package imports
from model_utils.models import TimeStampedModel

# Local imports
from applications.users.models import User


# Create your models here.
class ShiftCategory(TimeStampedModel):
    # name = models.CharField('Nombre', max_length=50, blank=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Shift Category'
        verbose_name_plural = 'Shift Categories'
        ordering = ['-created']
        db_table = 'shifts_shift_category'

    def __str__(self):
        return str(self.id) + ' ' + self.name + ': ' + self.description


class Shift(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shift_category = models.ForeignKey(ShiftCategory, on_delete=models.CASCADE)
    is_temporal = models.BooleanField(default=False)
    duration = models.PositiveSmallIntegerField()
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Shift'
        verbose_name_plural = 'Shifts'
        ordering = ['-user', '-created']

    def __str__(self):
        return (str(self.user.first_name) + ' ' + str(self.user.last_name) + ' ,Shift: ' + str(self.shift_category.name)
                + ' ,Status: ' + str(self.status) + ' ,Is temporal: ' + str(self.is_temporal)
                + ' ,Duration: ' + str(self.duration))


class DailyScheduler(TimeStampedModel):
    DAYS_OF_THE_WEEK = (
        (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'),
        (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'),
        (7, 'Sunday'))

    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    description = models.CharField(max_length=50, blank=True)
    day_of_the_week = models.PositiveSmallIntegerField(choices=DAYS_OF_THE_WEEK)
    group = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Daily Scheduler'
        verbose_name_plural = 'Daily Schedulers'
        ordering = ['-created']
        db_table = 'shifts_daily_scheduler'

    def __str__(self):
        return ('Day: ' + str(self.day_of_the_week) + ' ,Status: ' + str(self.status) +
                ' ,Description: ' + str(self.description) + ' ,Group: ' + str(self.group))


class Scheduler(TimeStampedModel):
    daily_scheduler = models.ForeignKey(DailyScheduler, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    description = models.CharField(max_length=50, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = 'Scheduler'
        verbose_name_plural = 'Schedulers'
        ordering = ['-created']

    def __str__(self):
        return ('Start time: ' + str(self.start_time) + ' ,End time: ' + str(self.end_time)
                + ' ,Description: ' + str(self.description) + ' ,Status: ' + str(self.status))

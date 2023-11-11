# Django imports
from django.core.exceptions import ValidationError
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


class MissingCategory(TimeStampedModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Missing Category'
        verbose_name_plural = 'Missing Categories'
        ordering = ['-created']
        db_table = 'shifts_missing_category'

    def __str__(self):
        return self.name


class Scheduler(TimeStampedModel):
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

    def clean(self):
        super().clean()
        if self.status:
            if Shift.objects.filter(user=self.user, status=True).exclude(pk=self.pk).exists():
                raise ValidationError(
                    'Solo puede haber un shift activo por usuario. Si desea crear un nuevo shift, desactive el anterior')
        else:
            # allow any combination
            pass

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (str(self.user.first_name) + ' ' + str(self.user.last_name) + ' ,Shift: ' + str(self.shift_category.name)
                + ' ,Status: ' + str(self.status) + ' ,Is temporal: ' + str(self.is_temporal)
                + ' ,Duration: ' + str(self.duration))


class DailyScheduler(TimeStampedModel):  # todo change to DalyShift
    DAYS_OF_THE_WEEK = (
        (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'),
        (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'),
        (7, 'Sunday'))

    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    description = models.CharField(max_length=50, blank=True)
    day_of_the_week = models.PositiveSmallIntegerField(choices=DAYS_OF_THE_WEEK)
    group = models.CharField(max_length=50, blank=True)
    shift_schedulers = models.ManyToManyField(Scheduler, limit_choices_to={'status': True})

    # todo An Clean to hours
    class Meta:
        verbose_name = 'Daily Scheduler'
        verbose_name_plural = 'Daily Schedulers'
        ordering = ['-day_of_the_week', '-created']
        db_table = 'shifts_daily_scheduler'
        unique_together = ('shift', 'day_of_the_week')

    def __str__(self):
        return ('Day: ' + str(self.day_of_the_week) + ' ' + str(self.shift.user.first_name) + ' ,Status: ' + str(
            self.status) +
                ' ,Description: ' + str(self.description) + ' ,Group: ' + str(self.group)) + ' ,ShiftStatus: ' + str(
            self.shift.status)


class Assistance(TimeStampedModel):
    CHOICES = ((0, 'did not assist'), (1, 'assisted '), (2, 'assisted but left early'),
               (4, 'arrived late'), (5, 'arrived late and left early'))  # todo Ver si se me ocurren mas opciones
    daily_scheduler = models.ForeignKey(DailyScheduler, on_delete=models.CASCADE)
    is_vacations = models.BooleanField(default=False)
    date = models.DateField()
    has_assisted = models.PositiveSmallIntegerField(choices=CHOICES, default=0)

    class Meta:
        verbose_name = 'Assistance'
        verbose_name_plural = 'Assistances'
        ordering = ['-date']
        unique_together = ('daily_scheduler', 'date')

    def __str__(self):
        return (('User: ' + str(self.daily_scheduler.shift.user.first_name)) + ' ,Date: ' + str(self.date)
                + ' ,Has assisted: ' + str(self.has_assisted))


class Missing(TimeStampedModel):
    assistance = models.OneToOneField(Assistance, on_delete=models.CASCADE)
    is_justified = models.BooleanField(default=False)
    reason = models.CharField(max_length=50, blank=True)
    worked_hours = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey(MissingCategory, on_delete=models.CASCADE, null=True, blank=True)
    missing_hours = models.ManyToManyField(Scheduler)

    # todo una validacion para que el missing coincida con el usuario

    class Meta:
        verbose_name = 'Missing'
        verbose_name_plural = 'Missings'
        ordering = ['-created']

    def __str__(self):
        return (('Is justified: ' + str(self.is_justified) + ' ,Reason: ' + str(self.reason)
                 + ' ,Worked hours: ' + str(self.worked_hours)) + ' ,Date: ' + str(self.assistance.date)
                + ' ,User: ' + str(self.assistance.daily_scheduler.shift.user.first_name))
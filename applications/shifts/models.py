# Django imports
from django.db import models

# Package imports
from model_utils.models import TimeStampedModel

# Local imports
from applications.users.models import User


# Create your models here.
class Category(TimeStampedModel):
    # name = models.CharField('Nombre', max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Shift Category'
        verbose_name_plural = 'Shift Categories'
        ordering = ['-created']

    def __str__(self):
        return str(self.id) + ' ' + self.name + ': ' + self.description


class Shift(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shift_category = models.OneToOneField(Category, on_delete=models.CASCADE)
    is_temporal = models.BooleanField(default=False)
    duration = models.SmallIntegerField()
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Shift'
        verbose_name_plural = 'Shifts'
        ordering = ['-user', '-created']

    def __str__(self):
        return (str(self.user.first_name) + ' ' + str(self.user.last_name) + ' ,Shift: ' + str(self.shift_category.name)
                + ' ,Status: ' + str(self.status) + ' ,Is temporal: ' + str(self.is_temporal)
                + ' ,Duration: ' + str(self.duration))

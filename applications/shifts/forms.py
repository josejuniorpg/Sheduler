# Django imports
from django import forms
from django.utils.translation import gettext_lazy as _


# Local imports
from .models import Shift, ShiftCategory
from ..users.models import User


class CreateShiftForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    # user = forms.ChoiceField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shift_category = forms.ModelChoiceField(queryset=ShiftCategory.objects.all(), required=True,
                                            widget=forms.Select(attrs={'class': 'form-control'}))
    is_temporal = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    duration = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.BooleanField(required=False, initial=True ,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Shift
        fields = (
            'user',
            'shift_category',
            'is_temporal',
            'duration',
            'status',
        )

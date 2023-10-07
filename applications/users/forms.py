# Django imports
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

# Local imports
from .models import User

class UserRegisterForm(UserCreationForm):
    GENDER_CHOICES_TRANSLATED = [('1', _('Men')),('2', _('Female')),('3', _('Others')),]

    email = forms.EmailField(label=_('Email'), required=True)
    first_name = forms.CharField(label=_('FirstName'), required=True)
    last_name = forms.CharField(label=_('LastName'), required=True)


    gender = forms.ChoiceField(choices=GENDER_CHOICES_TRANSLATED, label=_('Gender'))
    phone_number = forms.CharField(label=_('PhoneNumber'), required=True)
    profile_image = forms.ImageField(label=_('ProfileImage'))
    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'gender',
            'phone_number',
            'profile_image',
            'password1',
            'password2',
        )

class VerificationForm(forms.Form):
    code_verification = forms.CharField(required=True)

    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super().__init__(*args, **kwargs)

    def clean_code_verification(self):
        code = self.cleaned_data['code_verification']
        if len(code) == 6:
            active = User.objects.cod_validation(
                self.id_user,
                code
            )
            if not active:
                raise forms.ValidationError(_('TheCodeIsIncorrect'))
        else:
            raise forms.ValidationError(_('TheCodeIsIncorrect'))
        return code
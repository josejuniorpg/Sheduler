# Django imports
from django import forms
# from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

# Local imports
from .models import User


class UserRegisterForm(UserCreationForm):
    GENDER_CHOICES_TRANSLATED = [('1', _('Men')), ('2', _('Female')), ('3', _('Others')), ]

    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    # email = forms.EmailField(label=_('Email'), required=True)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES_TRANSLATED, label=_('Gender'),
                               widget=forms.Select(attrs={'class': 'form-select'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_image = forms.ImageField(label=_('ProfileImage'), required=False)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

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

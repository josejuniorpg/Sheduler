# Django imports
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

# Local imports
from .models import User

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(label=_('Password'),required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Password')
            }
        )
    )
    password2 = forms.CharField(label=_('RepeatPassword'),required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('RepeatPassword')
            }
        )
    )
    email = forms.EmailField(label=_('Email'), required=True)
    first_name = forms.CharField(label=_('FirstName'), required=True)
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
        )



    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', _('ThePasswordsDoNotMatch'))

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
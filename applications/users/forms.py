# Django imports
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, \
    PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _

# Package imports
from captcha.fields import ReCaptchaField

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
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = ReCaptchaField()

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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('This email address is already registered. Please choose another one.'))
        return email


class VerificationForm(forms.Form):
    code_verification = forms.CharField(label=_('Code Verification'), required=True,
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))

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


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Password')}))
    captcha = ReCaptchaField()


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='',
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'class': 'form-control', 'placeholder': 'Email'}),
    )
    captcha = ReCaptchaField(label='')


class UserPasswordRestConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control', 'placeholder': _('Password')}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control', 'placeholder': _('ConfirmPassword')}),
    )
    captcha = ReCaptchaField(label='')


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", 'class': 'form-control form-control-lg', 'placeholder': _('OldPassword')}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control form-control-lg', 'placeholder': _('Password')}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control form-control-lg', 'placeholder': _('ConfirmPassword')}),
    )
    captcha = ReCaptchaField()


class ProfileUpdateForm(forms.ModelForm):
    GENDER_CHOICES_TRANSLATED = [('1', _('Men')), ('2', _('Female')), ('3', _('Others')), ]

    first_name = forms.CharField(max_length=32, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=32, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=32, required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES_TRANSLATED, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'phone_number']
        exclude = '__all__'

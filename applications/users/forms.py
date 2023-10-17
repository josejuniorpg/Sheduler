# Django imports
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserModel, _unicode_ci_compare, \
    PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from  django.conf import settings

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
    profile_image = forms.ImageField(label=_('ProfileImage'), required=False)
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
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

# class PasswordResetForm1(PasswordResetForm):
#
#
#     def save(self, domain_override=None, subject_template_name='registration/password_reset_subject.txt',
#              email_template_name='registration/password_reset_email.html', use_https=False,
#              token_generator=None, from_email=None, request=None, html_email_template_name=None,
#              extra_email_context=None):
#
#         user = super().save(
#             domain_override, subject_template_name, email_template_name, use_https, token_generator,
#             from_email, request, html_email_template_name, extra_email_context
#         )
#         print('Email', from_email)
#         print('Domain', domain_override)
#
#         email = self.cleaned_data["email"]
#         if not domain_override:
#             current_site = get_current_site(request)
#             site_name = current_site.name
#             domain = current_site.domain
#         else:
#             site_name = domain = domain_override
#         print('El email', email)
#         user_email = User.objects.filter(email='yunipgdes@gmail.com').first()
#         context = {
#             "email": user_email.email,
#             "domain": domain,
#             "site_name": site_name,
#             "uid": urlsafe_base64_encode(force_bytes(user_email.id)),
#             "user": user_email,
#             "token": token_generator.make_token(user_email),
#             "protocol": "https" if use_https else "http",
#             **(extra_email_context or {}),
#         }
#         Urls = f'{context["protocol"]}://{context["domain"]}/password-reset-confirm/{context["uid"]}/{context["token"]}'
#         print('Urls', Urls)
#
#         def send_email_verify_code(id=None):
#             user = get_object_or_404(User, id=id)
#             subject = _('Verification Code') + '  ' + _('ForEmail') + '  ' + user.first_name
#             message = (
#                 f'{_("Verification Code")}:  {user.code_verification} \n{_("ForEmail")} {user.first_name}\n'
#                 f'Url {Urls}'
#             )
#             email_sender = settings.EMAIL_HOST_USER
#             send_mail(subject, message, email_sender, [user.email, ])
#
#         subject = loader.render_to_string(subject_template_name, context)
#         # Email subject *must not* contain newlines
#         subject = "".join(subject.splitlines())
#         body = loader.render_to_string(email_template_name, context)
#
#         email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
#         if html_email_template_name is not None:
#             html_email = loader.render_to_string(html_email_template_name, context)
#             email_message.attach_alternative(html_email, "text/html")
#
#         email_message.send()
#
#         send_email_verify_code(user_email.id)
#         return user
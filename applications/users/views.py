# Django imports
from django.contrib.auth.views import LoginView, PasswordResetView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Packages imports
from django_ratelimit.decorators import ratelimit

# Local imports
from applications.users.forms import (UserRegisterForm, VerificationForm, UserLoginForm,
                                      UserResetPasswordForm)
from applications.users.functions import (code_generator, send_again_email_verify_code,
                                          send_email_verify_code)
from applications.users.mixins import AnonymousRequiredMixin
from applications.users.models import User


# View Classes
class UserRegisterView(AnonymousRequiredMixin, FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    @method_decorator(ratelimit(key='user_or_ip', rate='5/m', block=True))
    def get(self, request):
        return super().get(request)  # todo Configure the page error

    @method_decorator(ratelimit(key='user_or_ip', rate='5/m', block=True))
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)  # todo Configure the page error

    def form_valid(self, form):
        try:
            # Generate the code
            code = code_generator()
            #
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                gender=form.cleaned_data['gender'],
                phone_number=form.cleaned_data['phone_number'],
                code_verification=code,
            )
            if user:
                # Add Profile Image
                User.objects.create_user_profile_image(user, form.cleaned_data['profile_image'])
                # Send email
                send_email_verify_code(user.id)

            return HttpResponseRedirect(
                reverse_lazy(
                    'users_app:verification-user',
                    kwargs={'pk': user.id}
                )
            )
        except Exception as e:  # todo Configure the page error,
            return HttpResponse(f"Error;    {e}", status=500)


class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    context_object_name = 'user'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'],
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, id=self.kwargs['pk'])
        context['user'] = User.objects.filter(pk=user.pk).values('first_name', 'profile_image', 'is_active',
                                                                 'id').first()
        return context

    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs['pk']).update(
            is_active=True
        )
        return super().form_valid(form)

    def get_success_url(self):
        current_url = reverse_lazy('users_app:verification-user', kwargs={'pk': self.kwargs['pk']})
        return current_url


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def form_invalid(self, form):
        user = User.objects.filter(email=form.cleaned_data['username']).first()
        if user and not user.is_active:
            messages.error(self.request, _('User Inactive. Please Verify your account'))
            return HttpResponseRedirect(
                reverse_lazy(
                    'users_app:verification-user',
                    kwargs={'pk': user.id}
                )
            )
        messages.error(self.request, _('Invalid credentials. Please try again.'))
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home_app:home')


class UserResetPasswordView(PasswordResetView):
    template_name = 'users/password_reset.html',
    html_email_template_name = 'users/password_reset_email.html'
    from_email = settings.EMAIL_HOST_USER
    form_class = UserResetPasswordForm
    success_url = reverse_lazy('users_app:password-reset-done')
    email_template_name = 'users/password_reset_email.html',


# View Functions
@ratelimit(key='user_or_ip', rate='5/m', block=True)
def send_again_email_view(request, pk=None):
    send_again_email_verify_code(pk)
    return HttpResponseRedirect(
        reverse_lazy(
            'users_app:verification-user',
            kwargs={'pk': pk}
        )
    )

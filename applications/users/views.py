# Django imports
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy

# Local imports
from applications.users.forms import UserRegisterForm, VerificationForm
from applications.users.functions import code_generator
from applications.users.mixins import AnonymousRequiredMixin
from applications.users.models import User


class UserRegisterView(AnonymousRequiredMixin, FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

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
                code_verification=code
            )
            if user:
                User.objects.create_user_profile_image(user, form.cleaned_data['profile_image'])
            # # enviar el codigo al email del user  #todo Mail Send
            # subject = 'Confrimacion d eemail'
            # message = 'Codigo de verificacion: ' + code
            # email_remitente = 'neunapp.cursos@gmail.com'
            # #
            # send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'], ])
            # # redirigir a pantalla de valdiacion

            return HttpResponseRedirect(
                reverse_lazy(
                    'users_app:verification-user',
                    kwargs={'pk': user.id}
                )
            )
        except Exception as e:
            return HttpResponse(f"Error;    {e}", status=500)


class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    # success_url = reverse_lazy('users_app:user-login')
    success_url = '/'
    context_object_name = 'user'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'],
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs['pk']).update(
            is_active=True
        )
        return super().form_valid(form)

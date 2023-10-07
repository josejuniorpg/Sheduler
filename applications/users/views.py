# Django imports
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy, reverse

# Local imports
from applications.users.forms import UserRegisterForm
from applications.users.functions import code_generator
from applications.users.models import User


class UserRegisterView(FormView):
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
                User.objects.create_user_profile_image(user,form.cleaned_data['profile_image'])
            # # enviar el codigo al email del user
            # subject = 'Confrimacion d eemail'
            # message = 'Codigo de verificacion: ' + code
            # email_remitente = 'neunapp.cursos@gmail.com'
            # #
            # send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'], ])
            # # redirigir a pantalla de valdiacion
            # return HttpResponseRedirect(
            #     reverse(
            #         'users_app:user-verification',
            #         kwargs={'pk': usuario.id}
            #     )
            # )
            return HttpResponse("Contenido de la respuesta", status=200)
        except Exception as e:
            return HttpResponse(f"Error {e}", status=500)


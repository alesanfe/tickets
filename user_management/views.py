from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from user_management.forms import CustomUserCreationForm
from user_management.models import User


# Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('home')


# Vista para registro de usuario
def signin_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.verify_email = False
            user.save()

            # Generar el token único
            token = default_token_generator.make_token(user)

            # Generar la URL de verificación por correo electrónico
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verify_url = reverse('verify_email', args=[uid, token])

            # Enviar el correo electrónico de verificación
            current_site = get_current_site(request)
            mail_subject = 'Verificación de correo electrónico'
            message = render_to_string('registration/verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'verify_url': verify_url,
            })

            if '@us.es' in user.email:
                send_mail(mail_subject, message, 'noreply@example.com', [user.email])
            return redirect('home')
        print(form.error_messages)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signin.html', {'form': form})


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.verify_email = True
        user.save()
        return render(request, 'registration/verification_success.html')
    else:
        return render(request, 'registration/verification_error.html')



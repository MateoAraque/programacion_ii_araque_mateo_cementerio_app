from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from cementerio.forms import RegistroForm
from cementerio.permisos import GRUPO_CONSULTOR


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Todo usuario nuevo entra como "consultor" (mínimo privilegio)
            grupo, _ = Group.objects.get_or_create(name=GRUPO_CONSULTOR)
            user.groups.add(grupo)
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}. Tu cuenta fue creada.')
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = RegistroForm()
    return render(request, 'cementerio/authentication/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        siguiente = request.POST.get('next', '')
        # Evita "open redirect": solo se acepta una URL de este mismo sitio
        if siguiente and url_has_allowed_host_and_scheme(
            siguiente, allowed_hosts={request.get_host()}, require_https=request.is_secure()
        ):
            return redirect(siguiente)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'cementerio/authentication/login.html', {'form': form})


@require_POST   # el cierre de sesión solo se atiende por POST
def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect(settings.LOGOUT_REDIRECT_URL)

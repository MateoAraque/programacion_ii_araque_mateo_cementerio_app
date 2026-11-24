from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from cementerio.models import Difunto, Sector, Servicio, Tumba


@login_required
def home_view(request):
    contexto = {
        'total_sectores': Sector.objects.count(),
        'total_difuntos': Difunto.objects.count(),
        'total_tumbas': Tumba.objects.count(),
        'total_servicios': Servicio.objects.count(),
    }
    return render(request, 'cementerio/home.html', contexto)

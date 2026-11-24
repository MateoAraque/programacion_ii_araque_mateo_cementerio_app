from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from cementerio.forms import TumbaForm
from cementerio.models import Sector, Tumba
from cementerio.permisos import marcar_propiedad, puede_modificar


@login_required
@permission_required('cementerio.view_tumba', raise_exception=True)
def tumba_list(request):
    q = request.GET.get('q', '').strip()
    sector_id = request.GET.get('sector_id', '').strip()
    estado = request.GET.get('estado', '').strip()

    # select_related (FK) y prefetch_related (M2M) evitan consultas repetidas
    tumbas = Tumba.objects.select_related('sector').prefetch_related('difuntos')
    if q:
        tumbas = tumbas.filter(
            Q(codigo__icontains=q)
            | Q(sector__nombre__icontains=q)
            | Q(difuntos__apellidos__icontains=q)
            | Q(difuntos__nombres__icontains=q)
        ).distinct()
    if sector_id.isdigit():
        tumbas = tumbas.filter(sector_id=sector_id)
    if estado in Tumba.Estado.values:
        tumbas = tumbas.filter(estado=estado)

    return render(request, 'cementerio/tumbas/tumba_list.html', {
        'tumbas': marcar_propiedad(request.user, list(tumbas)),
        'sectores': Sector.objects.all(),
        'estados': Tumba.Estado.choices,
        'q': q, 'sector_id': sector_id, 'estado': estado,
    })


@login_required
@permission_required('cementerio.view_tumba', raise_exception=True)
def tumba_detail(request, pk):
    tumba = get_object_or_404(Tumba.objects.select_related('sector'), pk=pk)
    return render(request, 'cementerio/tumbas/tumba_detail.html', {
        'tumba': tumba,
        'difuntos': tumba.difuntos.all(),
        'servicios': tumba.servicios.all(),
        'puede_modificar': puede_modificar(request.user, tumba),
    })


@login_required
@permission_required('cementerio.add_tumba', raise_exception=True)
def tumba_create(request):
    if request.method == 'POST':
        form = TumbaForm(request.POST)
        if form.is_valid():
            tumba = form.save(commit=False)
            tumba.creado_por = request.user
            tumba.save()
            form.save_m2m()   # con commit=False hay que guardar el ManyToMany aparte
            messages.success(request, 'Tumba creada exitosamente.')
            return redirect('tumba_list')
    else:
        form = TumbaForm()
    return render(request, 'cementerio/tumbas/formulario.html', {'form': form, 'titulo': 'Nueva tumba'})


@login_required
@permission_required('cementerio.change_tumba', raise_exception=True)
def tumba_update(request, pk):
    tumba = get_object_or_404(Tumba, pk=pk)
    if not puede_modificar(request.user, tumba):   # regla de propiedad
        raise PermissionDenied
    if request.method == 'POST':
        form = TumbaForm(request.POST, instance=tumba)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tumba actualizada exitosamente.')
            return redirect('tumba_list')
    else:
        form = TumbaForm(instance=tumba)
    return render(request, 'cementerio/tumbas/formulario.html', {'form': form, 'titulo': 'Editar tumba'})


@login_required
@permission_required('cementerio.delete_tumba', raise_exception=True)
def tumba_delete(request, pk):
    tumba = get_object_or_404(Tumba, pk=pk)
    if not puede_modificar(request.user, tumba):
        raise PermissionDenied
    if request.method == 'POST':
        tumba.delete()
        messages.success(request, 'Tumba eliminada exitosamente.')
        return redirect('tumba_list')
    return render(request, 'cementerio/tumbas/tumba_confirm_delete.html', {'tumba': tumba})

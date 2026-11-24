from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from cementerio.forms import ServicioForm
from cementerio.models import Servicio
from cementerio.permisos import marcar_propiedad, puede_modificar


@login_required
@permission_required('cementerio.view_servicio', raise_exception=True)
def servicio_list(request):
    servicios = Servicio.objects.select_related('tumba', 'tumba__sector')
    return render(request, 'cementerio/servicios/servicio_list.html', {
        'servicios': marcar_propiedad(request.user, list(servicios)),
    })


@login_required
@permission_required('cementerio.view_servicio', raise_exception=True)
def servicio_detail(request, pk):
    servicio = get_object_or_404(Servicio.objects.select_related('tumba', 'tumba__sector'), pk=pk)
    return render(request, 'cementerio/servicios/servicio_detail.html', {
        'servicio': servicio,
        'puede_modificar': puede_modificar(request.user, servicio),
    })


@login_required
@permission_required('cementerio.add_servicio', raise_exception=True)
def servicio_create(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.creado_por = request.user
            servicio.save()
            messages.success(request, 'Servicio registrado exitosamente.')
            return redirect('servicio_list')
    else:
        form = ServicioForm()
    return render(request, 'cementerio/servicios/formulario.html', {'form': form, 'titulo': 'Nuevo servicio'})


@login_required
@permission_required('cementerio.change_servicio', raise_exception=True)
def servicio_update(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if not puede_modificar(request.user, servicio):
        raise PermissionDenied
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio actualizado exitosamente.')
            return redirect('servicio_list')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'cementerio/servicios/formulario.html', {'form': form, 'titulo': 'Editar servicio'})


@login_required
@permission_required('cementerio.delete_servicio', raise_exception=True)
def servicio_delete(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if not puede_modificar(request.user, servicio):
        raise PermissionDenied
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado exitosamente.')
        return redirect('servicio_list')
    return render(request, 'cementerio/servicios/servicio_confirm_delete.html', {'servicio': servicio})

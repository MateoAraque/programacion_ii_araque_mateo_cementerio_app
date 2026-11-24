from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from cementerio.forms import DifuntoForm
from cementerio.models import Difunto
from cementerio.permisos import marcar_propiedad, puede_modificar


@login_required
@permission_required('cementerio.view_difunto', raise_exception=True)
def difunto_list(request):
    q = request.GET.get('q', '').strip()
    difuntos = Difunto.objects.all()
    if q:
        difuntos = difuntos.filter(
            Q(nombres__icontains=q) | Q(apellidos__icontains=q) | Q(cedula__icontains=q)
        )
    difuntos = marcar_propiedad(request.user, list(difuntos))
    return render(request, 'cementerio/difuntos/difunto_list.html', {'difuntos': difuntos, 'q': q})


@login_required
@permission_required('cementerio.view_difunto', raise_exception=True)
def difunto_detail(request, pk):
    difunto = get_object_or_404(Difunto, pk=pk)
    tumbas = difunto.tumbas.select_related('sector')
    return render(request, 'cementerio/difuntos/difunto_detail.html', {
        'difunto': difunto, 'tumbas': tumbas,
        'puede_modificar': puede_modificar(request.user, difunto),
    })


@login_required
@permission_required('cementerio.add_difunto', raise_exception=True)
def difunto_create(request):
    if request.method == 'POST':
        form = DifuntoForm(request.POST)
        if form.is_valid():
            difunto = form.save(commit=False)
            difunto.creado_por = request.user
            difunto.save()
            messages.success(request, 'Difunto registrado exitosamente.')
            return redirect('difunto_list')
    else:
        form = DifuntoForm()
    return render(request, 'cementerio/difuntos/formulario.html', {'form': form, 'titulo': 'Registrar difunto'})


@login_required
@permission_required('cementerio.change_difunto', raise_exception=True)
def difunto_update(request, pk):
    difunto = get_object_or_404(Difunto, pk=pk)
    if not puede_modificar(request.user, difunto):
        raise PermissionDenied
    if request.method == 'POST':
        form = DifuntoForm(request.POST, instance=difunto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Difunto actualizado exitosamente.')
            return redirect('difunto_list')
    else:
        form = DifuntoForm(instance=difunto)
    return render(request, 'cementerio/difuntos/formulario.html', {'form': form, 'titulo': 'Editar difunto'})


@login_required
@permission_required('cementerio.delete_difunto', raise_exception=True)
def difunto_delete(request, pk):
    difunto = get_object_or_404(Difunto, pk=pk)
    if not puede_modificar(request.user, difunto):
        raise PermissionDenied
    if request.method == 'POST':
        difunto.delete()
        messages.success(request, 'Difunto eliminado exitosamente.')
        return redirect('difunto_list')
    return render(request, 'cementerio/difuntos/difunto_confirm_delete.html', {'difunto': difunto})

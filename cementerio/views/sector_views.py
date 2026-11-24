from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from cementerio.forms import SectorForm
from cementerio.models import Sector
from cementerio.permisos import marcar_propiedad, puede_modificar


@login_required
@permission_required('cementerio.view_sector', raise_exception=True)
def sector_list(request):
    sectores = marcar_propiedad(request.user, list(Sector.objects.all()))
    return render(request, 'cementerio/sectores/sector_list.html', {'sectores': sectores})


@login_required
@permission_required('cementerio.view_sector', raise_exception=True)
def sector_detail(request, pk):
    sector = get_object_or_404(Sector, pk=pk)
    tumbas = sector.tumbas.all()   # relación inversa (related_name='tumbas')
    return render(request, 'cementerio/sectores/sector_detail.html', {
        'sector': sector, 'tumbas': tumbas,
        'puede_modificar': puede_modificar(request.user, sector),
    })


@login_required
@permission_required('cementerio.add_sector', raise_exception=True)
def sector_create(request):
    if request.method == 'POST':
        form = SectorForm(request.POST)
        if form.is_valid():
            sector = form.save(commit=False)
            sector.creado_por = request.user   # quién lo creó (regla de propiedad)
            sector.save()
            messages.success(request, 'Sector creado exitosamente.')
            return redirect('sector_list')
    else:
        form = SectorForm()
    return render(request, 'cementerio/sectores/formulario.html', {'form': form, 'titulo': 'Nuevo sector'})


@login_required
@permission_required('cementerio.change_sector', raise_exception=True)
def sector_update(request, pk):
    sector = get_object_or_404(Sector, pk=pk)
    if not puede_modificar(request.user, sector):
        raise PermissionDenied
    if request.method == 'POST':
        form = SectorForm(request.POST, instance=sector)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sector actualizado exitosamente.')
            return redirect('sector_list')
    else:
        form = SectorForm(instance=sector)
    return render(request, 'cementerio/sectores/formulario.html', {'form': form, 'titulo': 'Editar sector'})


@login_required
@permission_required('cementerio.delete_sector', raise_exception=True)
def sector_delete(request, pk):
    sector = get_object_or_404(Sector, pk=pk)
    if not puede_modificar(request.user, sector):
        raise PermissionDenied
    if request.method == 'POST':   # solo elimina con POST
        try:
            sector.delete()
            messages.success(request, 'Sector eliminado exitosamente.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar el sector porque tiene tumbas asociadas.')
        return redirect('sector_list')
    return render(request, 'cementerio/sectores/sector_confirm_delete.html', {'sector': sector})

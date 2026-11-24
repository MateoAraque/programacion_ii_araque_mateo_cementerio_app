from django.urls import path

from cementerio.views import (
    sector_list, sector_detail, sector_create, sector_update, sector_delete,
)

urlpatterns = [
    path('sectores/', sector_list, name='sector_list'),
    path('sectores/nuevo/', sector_create, name='sector_create'),
    path('sectores/<int:pk>/', sector_detail, name='sector_detail'),
    path('sectores/<int:pk>/editar/', sector_update, name='sector_update'),
    path('sectores/<int:pk>/eliminar/', sector_delete, name='sector_delete'),
]

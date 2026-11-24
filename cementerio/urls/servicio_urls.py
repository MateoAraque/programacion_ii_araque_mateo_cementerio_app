from django.urls import path

from cementerio.views import (
    servicio_list, servicio_detail, servicio_create, servicio_update, servicio_delete,
)

urlpatterns = [
    path('servicios/', servicio_list, name='servicio_list'),
    path('servicios/nuevo/', servicio_create, name='servicio_create'),
    path('servicios/<int:pk>/', servicio_detail, name='servicio_detail'),
    path('servicios/<int:pk>/editar/', servicio_update, name='servicio_update'),
    path('servicios/<int:pk>/eliminar/', servicio_delete, name='servicio_delete'),
]

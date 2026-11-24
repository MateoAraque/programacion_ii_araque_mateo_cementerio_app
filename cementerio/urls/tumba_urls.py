from django.urls import path

from cementerio.views import (
    tumba_list, tumba_detail, tumba_create, tumba_update, tumba_delete,
)

urlpatterns = [
    path('tumbas/', tumba_list, name='tumba_list'),
    path('tumbas/nuevo/', tumba_create, name='tumba_create'),
    path('tumbas/<int:pk>/', tumba_detail, name='tumba_detail'),
    path('tumbas/<int:pk>/editar/', tumba_update, name='tumba_update'),
    path('tumbas/<int:pk>/eliminar/', tumba_delete, name='tumba_delete'),
]

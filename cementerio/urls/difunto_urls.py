from django.urls import path

from cementerio.views import (
    difunto_list, difunto_detail, difunto_create, difunto_update, difunto_delete,
)

urlpatterns = [
    path('difuntos/', difunto_list, name='difunto_list'),
    path('difuntos/nuevo/', difunto_create, name='difunto_create'),
    path('difuntos/<int:pk>/', difunto_detail, name='difunto_detail'),
    path('difuntos/<int:pk>/editar/', difunto_update, name='difunto_update'),
    path('difuntos/<int:pk>/eliminar/', difunto_delete, name='difunto_delete'),
]

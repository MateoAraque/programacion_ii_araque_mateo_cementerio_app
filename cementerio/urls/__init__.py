# Reúne las URLs de cada entidad en una sola lista
from django.urls import include, path

urlpatterns = [
    path('', include('cementerio.urls.home_urls')),
    path('', include('cementerio.urls.auth_urls')),
    path('', include('cementerio.urls.sector_urls')),
    path('', include('cementerio.urls.difunto_urls')),
    path('', include('cementerio.urls.tumba_urls')),
    path('', include('cementerio.urls.servicio_urls')),
]

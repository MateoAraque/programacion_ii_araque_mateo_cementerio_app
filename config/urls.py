from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cementerio.urls')),   # cementerio/urls/__init__.py reúne todas
]

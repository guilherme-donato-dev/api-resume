# core/urls.py

from django.contrib import admin
from django.urls import path, include # Adicione o 'include'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Diga ao Django para incluir as URLs do app "summarizer"
    # no caminho "api/"
    path('api/', include('summarizer.urls')),
]
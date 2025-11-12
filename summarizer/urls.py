# summarizer/urls.py

from django.urls import path
from .views import SummarizeView

urlpatterns = [
    # Quando alguém acessar /api/summarize/, chame a SummarizeView
    path('summarize/', SummarizeView.as_view(), name='summarize'),
]
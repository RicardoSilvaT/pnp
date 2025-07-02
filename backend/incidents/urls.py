# incidencias/urls.py
from django.urls import path
from .views import UploadIncidenciasView, ListarIncidenciasView, DeleteBatchIncidenciasView

urlpatterns = [
    path('upload/',       UploadIncidenciasView.as_view()),
    path('list/',         ListarIncidenciasView.as_view()),
    path('delete-batch/', DeleteBatchIncidenciasView.as_view()),
]
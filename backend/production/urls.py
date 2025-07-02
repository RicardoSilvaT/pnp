# production/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


# Crear router para las APIs
router = DefaultRouter()


# Registrar ViewSets de catálogos
router.register(r'tipos-documento', views.TipoDocumentoViewSet, basename='tipodocumento')
router.register(r'departamentos', views.DepartamentoViewSet, basename='departamento')
router.register(r'provincias', views.ProvinciaViewSet, basename='provincia')
router.register(r'distritos', views.DistritoViewSet, basename='distrito')
router.register(r'delitos-generales', views.DelitoGeneralViewSet, basename='delitogeneral')
router.register(r'delitos-especificos', views.DelitoEspecificoViewSet, basename='delitoespecifico')
router.register(r'sub-tipos-delito', views.SubTipoDelitoViewSet, basename='subtipodelito')


# Registrar ViewSets de plantillas
router.register(r'plantillas', views.PlantillaViewSet, basename='plantilla')
router.register(r'campos-plantilla', views.CampoPlantillaViewSet, basename='campoplantilla')


# Registrar ViewSet principal de formularios
router.register(r'formularios', views.SubmisionFormularioViewSet, basename='submisionformulario')


# Registrar ViewSets especializados
router.register(r'ubicaciones', views.UbicacionJerarquicaViewSet, basename='ubicacion')
router.register(r'catalogos', views.CatalogoCompletoViewSet, basename='catalogo')  # ← Esta línea debe estar


# URLs
urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from production.views import (
    # Ubicación
    DepartamentoViewSet, ProvinciaViewSet, DistritoViewSet,
    # Personas
    NacionalidadViewSet, TipoDocumentoViewSet, TipoRequisitoriaViewSet,
    # Delitos
    DelitoFueroViewSet, DelitoGeneralViewSet, DelitoEspecificoViewSet, DelitoSubtipoViewSet,
    # Estructura Policial
    DireccionPolicialViewSet, DireccionEspecializadaViewSet, DivisionPolicialViewSet,
    DepartamentoPolicialViewSet, UnidadPolicialViewSet,
    # Armas
    CategoriaArmaViewSet, TipoArmaViewSet,
    # Judicial
    SituacionDetenidoViewSet, FiscaliaViewSet
)

# Router para tablas de referencia
router = DefaultRouter()

# =============================================================================
# ENDPOINTS DE UBICACIÓN GEOGRÁFICA
# =============================================================================
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'provincias', ProvinciaViewSet, basename='provincia')
router.register(r'distritos', DistritoViewSet, basename='distrito')

# =============================================================================
# ENDPOINTS DE DATOS DE PERSONAS
# =============================================================================
router.register(r'nacionalidades', NacionalidadViewSet, basename='nacionalidad')
router.register(r'tipos-documento', TipoDocumentoViewSet, basename='tipo-documento')
router.register(r'tipos-requisitoria', TipoRequisitoriaViewSet, basename='tipo-requisitoria')

# =============================================================================
# ENDPOINTS DE DELITOS
# =============================================================================
router.register(r'delitos-fuero', DelitoFueroViewSet, basename='delito-fuero')
router.register(r'delitos-general', DelitoGeneralViewSet, basename='delito-general')
router.register(r'delitos-especifico', DelitoEspecificoViewSet, basename='delito-especifico')
router.register(r'delitos-subtipo', DelitoSubtipoViewSet, basename='delito-subtipo')

# =============================================================================
# ENDPOINTS DE ESTRUCTURA POLICIAL
# =============================================================================
router.register(r'direcciones-policiales', DireccionPolicialViewSet, basename='direccion-policial')
router.register(r'direcciones-especializadas', DireccionEspecializadaViewSet, basename='direccion-especializada')
router.register(r'divisiones-policiales', DivisionPolicialViewSet, basename='division-policial')
router.register(r'departamentos-policiales', DepartamentoPolicialViewSet, basename='departamento-policial')
router.register(r'unidades-policiales', UnidadPolicialViewSet, basename='unidad-policial')

# =============================================================================
# ENDPOINTS DE ARMAS
# =============================================================================
router.register(r'categorias-armas', CategoriaArmaViewSet, basename='categoria-arma')
router.register(r'tipos-armas', TipoArmaViewSet, basename='tipo-arma')

# =============================================================================
# ENDPOINTS JUDICIALES
# =============================================================================
router.register(r'situaciones-detenido', SituacionDetenidoViewSet, basename='situacion-detenido')
router.register(r'fiscalias', FiscaliaViewSet, basename='fiscalia')

# URLs finales
urlpatterns = [
    path('', include(router.urls)),
]

"""
DOCUMENTACIÓN DE ENDPOINTS DE REFERENCIA:

📍 UBICACIÓN GEOGRÁFICA:
- GET /api/production/reference/departamentos/ - Listar departamentos
- GET /api/production/reference/provincias/ - Listar provincias
- GET /api/production/reference/provincias/por_departamento/?departamento_id=1 - Provincias por departamento
- GET /api/production/reference/distritos/ - Listar distritos  
- GET /api/production/reference/distritos/por_provincia/?provincia_id=1 - Distritos por provincia

👤 DATOS DE PERSONAS:
- GET /api/production/reference/nacionalidades/ - Listar nacionalidades
- GET /api/production/reference/tipos-documento/ - Listar tipos de documento
- GET /api/production/reference/tipos-requisitoria/ - Listar tipos de requisitoria

⚖️ DELITOS (con filtros cascada):
- GET /api/production/reference/delitos-fuero/ - Listar fueros
- GET /api/production/reference/delitos-general/ - Listar delitos generales
- GET /api/production/reference/delitos-general/por_fuero/?fuero_id=1 - Por fuero
- GET /api/production/reference/delitos-especifico/ - Listar delitos específicos
- GET /api/production/reference/delitos-especifico/por_general/?general_id=1 - Por general
- GET /api/production/reference/delitos-subtipo/ - Listar subtipos
- GET /api/production/reference/delitos-subtipo/por_especifico/?especifico_id=1 - Por específico

🚔 ESTRUCTURA POLICIAL:
- GET /api/production/reference/direcciones-policiales/ - Listar direcciones principales
- GET /api/production/reference/direcciones-especializadas/ - Listar especializadas
- GET /api/production/reference/direcciones-especializadas/por_direccion/?direccion_id=1 - Por dirección
- GET /api/production/reference/divisiones-policiales/ - Listar divisiones
- GET /api/production/reference/departamentos-policiales/ - Listar departamentos policiales
- GET /api/production/reference/unidades-policiales/ - Listar unidades

🔫 ARMAS:
- GET /api/production/reference/categorias-armas/ - Listar categorías
- GET /api/production/reference/tipos-armas/ - Listar tipos
- GET /api/production/reference/tipos-armas/por_categoria/?categoria_id=1 - Por categoría

⚖️ JUDICIAL:
- GET /api/production/reference/situaciones-detenido/ - Listar situaciones
- GET /api/production/reference/fiscalias/ - Listar fiscalías

🔗 FILTROS GLOBALES:
- GET /api/production/filtros-cascada/?tipo=provincias_por_departamento&padre_id=1
- GET /api/production/filtros-cascada/?tipo=distritos_por_provincia&padre_id=1
- GET /api/production/filtros-cascada/?tipo=delitos_generales_por_fuero&padre_id=1
- GET /api/production/filtros-cascada/?tipo=delitos_especificos_por_general&padre_id=1
- GET /api/production/filtros-cascada/?tipo=delitos_subtipos_por_especifico&padre_id=1
- GET /api/production/filtros-cascada/?tipo=direcciones_especializadas_por_direccion&padre_id=1
- GET /api/production/filtros-cascada/?tipo=tipos_arma_por_categoria&padre_id=1
"""
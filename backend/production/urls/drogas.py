from django.urls import path, include
from rest_framework.routers import DefaultRouter
from production.views import (
    # Envoltorios
    PlantillaEnvPBCViewSet, PlantillaEnvCCViewSet, PlantillaEnvMarihuanaViewSet,
    # Kilogramos  
    PlantillaKgPBCViewSet, PlantillaKgCCViewSet, PlantillaKgMarihuanaViewSet,
    PlantillaKgLatexOpioViewSet, PlantillaKgDrogaSinteticaViewSet
)

# Router para formularios de drogas
router = DefaultRouter()

# =============================================================================
# ENDPOINTS DE ENVOLTORIOS
# =============================================================================
router.register(r'env-pbc', PlantillaEnvPBCViewSet, basename='env-pbc')
router.register(r'env-cc', PlantillaEnvCCViewSet, basename='env-cc')
router.register(r'env-marihuana', PlantillaEnvMarihuanaViewSet, basename='env-marihuana')

# =============================================================================
# ENDPOINTS DE KILOGRAMOS
# =============================================================================
router.register(r'kg-pbc', PlantillaKgPBCViewSet, basename='kg-pbc')
router.register(r'kg-cc', PlantillaKgCCViewSet, basename='kg-cc')
router.register(r'kg-marihuana', PlantillaKgMarihuanaViewSet, basename='kg-marihuana')
router.register(r'kg-latex-opio', PlantillaKgLatexOpioViewSet, basename='kg-latex-opio')
router.register(r'kg-droga-sintetica', PlantillaKgDrogaSinteticaViewSet, basename='kg-droga-sintetica')

# URLs finales
urlpatterns = [
    path('', include(router.urls)),
]

"""
DOCUMENTACIÓN DE ENDPOINTS DE DROGAS:

================================================================================
📦 ENVOLTORIOS DE DROGAS
================================================================================

ENV PBC - ENVOLTORIOS DE PASTA BÁSICA DE COCAÍNA:
- GET /api/production/drogas/env-pbc/ - Listar (serializer simplificado)
- POST /api/production/drogas/env-pbc/ - Crear nuevo
- GET /api/production/drogas/env-pbc/{id}/ - Obtener específico (serializer completo)
- PUT /api/production/drogas/env-pbc/{id}/ - Actualizar completo
- PATCH /api/production/drogas/env-pbc/{id}/ - Actualizar parcial
- DELETE /api/production/drogas/env-pbc/{id}/ - Eliminar

ENV CC - ENVOLTORIOS DE CLORHIDRATO DE COCAÍNA:
- GET /api/production/drogas/env-cc/ - Listar
- POST /api/production/drogas/env-cc/ - Crear nuevo
- GET /api/production/drogas/env-cc/{id}/ - Obtener específico
- PUT /api/production/drogas/env-cc/{id}/ - Actualizar completo
- PATCH /api/production/drogas/env-cc/{id}/ - Actualizar parcial
- DELETE /api/production/drogas/env-cc/{id}/ - Eliminar

ENV MARIHUANA - ENVOLTORIOS DE MARIHUANA:
- GET /api/production/drogas/env-marihuana/ - Listar
- POST /api/production/drogas/env-marihuana/ - Crear nuevo
- GET /api/production/drogas/env-marihuana/{id}/ - Obtener específico
- PUT /api/production/drogas/env-marihuana/{id}/ - Actualizar completo
- PATCH /api/production/drogas/env-marihuana/{id}/ - Actualizar parcial
- DELETE /api/production/drogas/env-marihuana/{id}/ - Eliminar

================================================================================
⚖️ KILOGRAMOS DE DROGAS
================================================================================

KG PBC - KILOGRAMOS DE PASTA BÁSICA DE COCAÍNA:
- GET /api/production/drogas/kg-pbc/ - Listar
- POST /api/production/drogas/kg-pbc/ - Crear nuevo
- GET /api/production/drogas/kg-pbc/{id}/ - Obtener específico
- PUT /api/production/drogas/kg-pbc/{id}/ - Actualizar completo
- PATCH /api/production/drogas/kg-pbc/{id}/ - Actualizar parcial
- DELETE /api/production/drogas/kg-pbc/{id}/ - Eliminar

KG CC - KILOGRAMOS DE CLORHIDRATO DE COCAÍNA:
- GET /api/production/drogas/kg-cc/ - Listar
- POST /api/production/drogas/kg-cc/ - Crear nuevo
- GET /api/production/drogas/kg-cc/{id}/ - Obtener específico
- PUT /api/production/drogas/kg-cc/{id}/ - Actualizar completo
- PATCH /api/production/drogas/kg-cc/{id}/ - Actualizar parcial
- DELETE /api/production/drogas/kg-cc/{id}/ - Eliminar

KG MARIHUANA - KILOGRAMOS DE MARIHUANA:
- GET /api/production/drogas/kg-marihuana/ - Listar
- POST /api/production/drogas/kg-marihuana/ - Crear nuevo
- GET /api/production/drogas/kg-marihuana/{id}/ - Obtener específico
- PUT /api/production/drogas/kg-marihuana/{id}/ - Actualizar completo
- PATCH /api/production/drogas/kg-marihuana/{id}/ - Actualizar parcial
- DELETE /api/production/drogas/kg-marihuana/{id}/ - Eliminar

KG LÁTEX OPIO - KILOGRAMOS DE LÁTEX DE OPIO:
- GET /api/production/drogas/kg-latex-opio/ - Listar
- POST /api/production/drogas/kg-latex-opio/ - Crear nuevo
- GET /api/production/drogas/kg-latex-opio/{id}/ - Obtener específico
- PUT /api/production/drogas/kg-latex-opio/{id}/ - Actualizar completo
- PATCH /api/production/drogas/kg-latex-opio/{id}/ - Actualizar parcial
- DELETE /api/production/drogas/kg-latex-opio/{id}/ - Eliminar

KG DROGA SINTÉTICA - KILOGRAMOS DE DROGA SINTÉTICA:
- GET /api/production/drogas/kg-droga-sintetica/ - Listar
- POST /api/production/drogas/kg-droga-sintetica/ - Crear nuevo
- GET /api/production/drogas/kg-droga-sintetica/{id}/ - Obtener específico
- PUT /api/production/drogas/kg-droga-sintetica/{id}/ - Actualizar completo
- PATCH /api/production/drogas/kg-droga-sintetica/{id}/ - Actualizar parcial
- DELETE /api/production/drogas/kg-droga-sintetica/{id}/ - Eliminar

================================================================================
📊 ESTADÍSTICAS Y REPORTES (TODOS LOS FORMULARIOS DE DROGAS)
================================================================================

ENDPOINTS COMUNES PARA TODOS:
- GET /api/production/drogas/{formulario}/estadisticas/ - Estadísticas generales
- GET /api/production/drogas/{formulario}/estadisticas_drogas/ - Estadísticas específicas
- GET /api/production/drogas/{formulario}/reporte_resumen/ - Reporte resumen
- GET /api/production/drogas/{formulario}/busqueda_avanzada/ - Búsqueda avanzada
- GET /api/production/drogas/{formulario}/exportar_excel/ - Preparar exportación

ESTADÍSTICAS CONSOLIDADAS:
- GET /api/production/estadisticas-drogas/ - Estadísticas de todas las drogas consolidadas
  Parámetros: ?fecha_desde=2024-01-01&fecha_hasta=2024-12-31&departamento_id=1

RANKINGS:
- GET /api/production/ranking-incautaciones/?tipo=departamento&limite=10
- GET /api/production/ranking-incautaciones/?tipo=unidad&limite=10

================================================================================
🔍 FILTROS COMUNES PARA TODAS LAS DROGAS
================================================================================

FILTROS BÁSICOS:
?departamento=1&provincia=1&distrito=1&direccion_policial=1&tipo_intervencion=OPERATIVO

FILTROS POR CANTIDAD:
ENVOLTORIOS: ?cantidad_unidades=5&cantidad_unidades__gte=10&cantidad_unidades__lte=100
KILOGRAMOS: ?cantidad_kilogramos=5.5&cantidad_kilogramos__gte=1.0&cantidad_kilogramos__lte=50.0

BÚSQUEDA DE TEXTO:
?search=sicpip

ORDENAMIENTO:
?ordering=-fecha_incautacion&ordering=cantidad_unidades&ordering=-cantidad_kilogramos

PAGINACIÓN:
?page=1&page_size=20

================================================================================
🎯 BÚSQUEDA AVANZADA
================================================================================

GET /api/production/drogas/{formulario}/busqueda_avanzada/
Parámetros:
- fecha_desde=2024-01-01
- fecha_hasta=2024-12-31
- departamento_id=1
- provincia_id=1
- distrito_id=1
- direccion_policial_id=1
- texto_libre=operativo

RESPUESTA LISTADO SIMPLIFICADO:
{
  "id": 1,
  "numero_registro": 1,
  "fecha_incautacion": "2024-06-27",
  "cantidad_unidades": 15,          // Solo para envoltorios
  "cantidad_kilogramos": "5.750",   // Solo para kilogramos
  "departamento_nombre": "LIMA",
  "direccion_policial_sigla": "DIRNIC",
  "tipo_intervencion": "OPERATIVO"
}

RESPUESTA DETALLE COMPLETO:
{
  "id": 1,
  "numero_registro": 1,
  "fecha_incautacion": "2024-06-27",
  "hora_incautacion": "14:30:00",
  "cantidad_unidades": 15,
  "ubicacion_completa": { ... },
  "unidad_policial_completa": { ... },
  "nota_informativa_sicpip": "...",
  "tipo_intervencion": "OPERATIVO",
  "created_at": "2024-06-27T14:30:00Z",
  "created_by": "usuario1"
}
"""
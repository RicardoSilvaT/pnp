from django.urls import path, include
from rest_framework.routers import DefaultRouter
from production.views import (
    PlantillaRQViewSet, PlantillaDetenidosViewSet, PlantillaMenoresRetenidosViewSet
)

# Router para formularios de personas
router = DefaultRouter()

# =============================================================================
# ENDPOINTS DE FORMULARIOS DE PERSONAS
# =============================================================================
router.register(r'rq', PlantillaRQViewSet, basename='rq')
router.register(r'detenidos', PlantillaDetenidosViewSet, basename='detenidos')
router.register(r'menores', PlantillaMenoresRetenidosViewSet, basename='menores')

# URLs finales
urlpatterns = [
    path('', include(router.urls)),
]

"""
DOCUMENTACIÓN DE ENDPOINTS DE PERSONAS:

📋 RQ - PERSONAS DETENIDAS POR REQUISITORIAS:
- GET /api/production/personas/rq/ - Listar todas las RQ (con paginación)
- POST /api/production/personas/rq/ - Crear nueva RQ
- GET /api/production/personas/rq/{id}/ - Obtener RQ específica
- PUT /api/production/personas/rq/{id}/ - Actualizar RQ completa
- PATCH /api/production/personas/rq/{id}/ - Actualizar RQ parcial
- DELETE /api/production/personas/rq/{id}/ - Eliminar RQ

📊 ESTADÍSTICAS Y REPORTES RQ:
- GET /api/production/personas/rq/estadisticas/ - Estadísticas generales
- GET /api/production/personas/rq/estadisticas_personas/ - Estadísticas de personas
- GET /api/production/personas/rq/estadisticas_rq/ - Estadísticas específicas RQ
- GET /api/production/personas/rq/reporte_resumen/ - Reporte resumen
- GET /api/production/personas/rq/busqueda_avanzada/ - Búsqueda avanzada

🔍 BÚSQUEDAS ESPECÍFICAS RQ:
- GET /api/production/personas/rq/buscar_por_documento/?numero_documento=12345678
- GET /api/production/personas/rq/exportar_excel/ - Preparar exportación

FILTROS DISPONIBLES RQ:
?genero=MASCULINO&edad=25&nacionalidad=1&tipo_documento=1&departamento=1
&provincia=1&distrito=1&tipo_requisitoria=1&esta_en_lista_mas_buscados=SÍ
&es_funcionario_publico=FUNCIONARIO_PUBLICO&direccion_policial=1

BÚSQUEDA DE TEXTO RQ:
?search=garcia lopez juan

ORDENAMIENTO RQ:
?ordering=-fecha_detencion&ordering=apellido_paterno

================================================================================

📋 DETENIDOS - PERSONAS DETENIDAS POR DIVERSOS DELITOS:
- GET /api/production/personas/detenidos/ - Listar todos los detenidos
- POST /api/production/personas/detenidos/ - Crear nuevo detenido
- GET /api/production/personas/detenidos/{id}/ - Obtener detenido específico
- PUT /api/production/personas/detenidos/{id}/ - Actualizar detenido completo
- PATCH /api/production/personas/detenidos/{id}/ - Actualizar detenido parcial
- DELETE /api/production/personas/detenidos/{id}/ - Eliminar detenido

📊 ESTADÍSTICAS Y REPORTES DETENIDOS:
- GET /api/production/personas/detenidos/estadisticas/ - Estadísticas generales
- GET /api/production/personas/detenidos/estadisticas_personas/ - Estadísticas de personas
- GET /api/production/personas/detenidos/estadisticas_detenidos/ - Estadísticas específicas
- GET /api/production/personas/detenidos/reporte_resumen/ - Reporte resumen
- GET /api/production/personas/detenidos/busqueda_avanzada/ - Búsqueda avanzada

🔍 BÚSQUEDAS ESPECÍFICAS DETENIDOS:
- GET /api/production/personas/detenidos/buscar_por_organizacion/?nombre_organizacion=los_vengadores

FILTROS ADICIONALES DETENIDOS:
?motivo_detencion=FLAGRANCIA&es_integrante_bbcc_oocc=SÍ&categoria_arma=1
&situacion_detenido=1&fiscalia=1

================================================================================

📋 MENORES - MENORES RETENIDOS POR DIVERSOS DELITOS:
- GET /api/production/personas/menores/ - Listar todos los menores (edad < 18)
- POST /api/production/personas/menores/ - Crear nuevo menor
- GET /api/production/personas/menores/{id}/ - Obtener menor específico
- PUT /api/production/personas/menores/{id}/ - Actualizar menor completo
- PATCH /api/production/personas/menores/{id}/ - Actualizar menor parcial
- DELETE /api/production/personas/menores/{id}/ - Eliminar menor

📊 ESTADÍSTICAS Y REPORTES MENORES:
- GET /api/production/personas/menores/estadisticas/ - Estadísticas generales
- GET /api/production/personas/menores/estadisticas_personas/ - Estadísticas de personas
- GET /api/production/personas/menores/estadisticas_menores/ - Estadísticas específicas menores
- GET /api/production/personas/menores/reporte_menores_riesgo/ - Reporte de menores en riesgo
- GET /api/production/personas/menores/reporte_resumen/ - Reporte resumen
- GET /api/production/personas/menores/busqueda_avanzada/ - Búsqueda avanzada

FILTROS MENORES (sin funcionario_publico):
?genero=MASCULINO&edad=16&motivo_detencion=FLAGRANCIA&es_integrante_bbcc_oocc=SÍ

================================================================================

🔍 BÚSQUEDA AVANZADA COMÚN (todos los formularios):
GET /api/production/personas/{formulario}/busqueda_avanzada/
Parámetros:
- fecha_desde=2024-01-01
- fecha_hasta=2024-12-31
- departamento_id=1
- provincia_id=1
- distrito_id=1
- direccion_policial_id=1
- texto_libre=garcia lopez

📊 PAGINACIÓN:
- ?page=1&page_size=20 (por defecto: 20 registros por página)

🔢 FORMATO DE RESPUESTA:
{
  "count": 150,
  "next": "http://localhost:8000/api/production/personas/rq/?page=2",
  "previous": null,
  "results": [ ... ]
}
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from production.views import (
    # Funciones especiales que no son ViewSets
    filtros_cascada_global, estadisticas_drogas_consolidadas, ranking_incautaciones
)

# Router principal
router = DefaultRouter()

# Configuración base
app_name = 'production'

urlpatterns = [
    # URLs de tablas de referencia
    path('reference/', include('production.urls.reference')),
    
    # URLs de formularios de personas
    path('personas/', include('production.urls.personas')),
    
    # URLs de formularios de drogas
    path('drogas/', include('production.urls.drogas')),
    
    # Endpoints especiales globales
    path('filtros-cascada/', filtros_cascada_global, name='filtros_cascada_global'),
    path('estadisticas-drogas/', estadisticas_drogas_consolidadas, name='estadisticas_drogas_consolidadas'),
    path('ranking-incautaciones/', ranking_incautaciones, name='ranking_incautaciones'),
    
    # Incluir router principal (vacío por ahora, los routers específicos están en cada submódulo)
    path('', include(router.urls)),
]
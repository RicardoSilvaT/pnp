# Importar views base
from .base_views import (
    BaseFormularioViewSet, BaseReferenceViewSet, FiltrosCascadaMixin,
    BusquedaAvanzadaMixin, ReportesMixin, FormularioPersonasViewSet, FormularioDrogasViewSet
)

# Importar views de referencia
from .reference_views import (
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
    SituacionDetenidoViewSet, FiscaliaViewSet,
    # Función global de filtros
    filtros_cascada_global
)

# Importar views de personas
from .personas_views import (
    PlantillaRQViewSet, PlantillaDetenidosViewSet, PlantillaMenoresRetenidosViewSet
)

# Importar views de drogas
from .drogas_views import (
    # Envoltorios
    PlantillaEnvPBCViewSet, PlantillaEnvCCViewSet, PlantillaEnvMarihuanaViewSet,
    # Kilogramos
    PlantillaKgPBCViewSet, PlantillaKgCCViewSet, PlantillaKgMarihuanaViewSet,
    PlantillaKgLatexOpioViewSet, PlantillaKgDrogaSinteticaViewSet,
    # Funciones especiales
    estadisticas_drogas_consolidadas, ranking_incautaciones
)

# Lista de todos los viewsets y funciones disponibles
__all__ = [
    # Base
    'BaseFormularioViewSet', 'BaseReferenceViewSet', 'FiltrosCascadaMixin',
    'BusquedaAvanzadaMixin', 'ReportesMixin', 'FormularioPersonasViewSet', 'FormularioDrogasViewSet',
    
    # Referencia
    'DepartamentoViewSet', 'ProvinciaViewSet', 'DistritoViewSet',
    'NacionalidadViewSet', 'TipoDocumentoViewSet', 'TipoRequisitoriaViewSet',
    'DelitoFueroViewSet', 'DelitoGeneralViewSet', 'DelitoEspecificoViewSet', 'DelitoSubtipoViewSet',
    'DireccionPolicialViewSet', 'DireccionEspecializadaViewSet', 'DivisionPolicialViewSet',
    'DepartamentoPolicialViewSet', 'UnidadPolicialViewSet',
    'CategoriaArmaViewSet', 'TipoArmaViewSet',
    'SituacionDetenidoViewSet', 'FiscaliaViewSet',
    'filtros_cascada_global',
    
    # Personas
    'PlantillaRQViewSet', 'PlantillaDetenidosViewSet', 'PlantillaMenoresRetenidosViewSet',
    
    # Drogas
    'PlantillaEnvPBCViewSet', 'PlantillaEnvCCViewSet', 'PlantillaEnvMarihuanaViewSet',
    'PlantillaKgPBCViewSet', 'PlantillaKgCCViewSet', 'PlantillaKgMarihuanaViewSet',
    'PlantillaKgLatexOpioViewSet', 'PlantillaKgDrogaSinteticaViewSet',
    'estadisticas_drogas_consolidadas', 'ranking_incautaciones',
]
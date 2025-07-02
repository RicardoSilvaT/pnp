# Importar serializers base
from .base_serializers import (
    BaseFormularioSerializer, UbicacionMixin, UnidadPolicialMixin, 
    DelitoMixin, FormularioValidationMixin,
    SimpleReferenceSerializer, SimpleReferenceWithCodeSerializer, 
    SimpleReferenceWithSiglaSerializer,
    ProvinciaFiltradaSerializer, DistritoFiltradoSerializer,
    DelitoGeneralFiltradoSerializer, DelitoEspecificoFiltradoSerializer,
    DelitoSubtipoFiltradoSerializer, DireccionEspecializadaFiltradaSerializer,
    TipoArmaFiltradoSerializer
)

# Importar serializers de referencia
from .reference_serializers import (
    # Ubicación
    DepartamentoSerializer, ProvinciaSerializer, DistritoSerializer,
    # Personas
    NacionalidadSerializer, TipoDocumentoSerializer, TipoRequisitoriaSerializer,
    # Delitos
    DelitoFueroSerializer, DelitoGeneralSerializer, DelitoEspecificoSerializer, DelitoSubtipoSerializer,
    # Estructura Policial
    DireccionPolicialSerializer, DireccionEspecializadaSerializer, DivisionPolicialSerializer,
    DepartamentoPolicialSerializer, UnidadPolicialSerializer,
    # Armas
    CategoriaArmaSerializer, TipoArmaSerializer,
    # Judicial
    SituacionDetenidoSerializer, FiscaliaSerializer,
    # Filtros
    ProvinciasPorDepartamentoSerializer, DistritosPorProvinciaSerializer,
    DelitosGeneralesPorFueroSerializer, DelitosEspecificosPorGeneralSerializer,
    DelitosSubtiposPorEspecificoSerializer, DireccionesEspecializadasPorDireccionSerializer,
    TiposArmaPorCategoriaSerializer
)

# Importar serializers de personas
from .personas_serializers import (
    PlantillaRQSerializer, PlantillaDetenidosSerializer, PlantillaMenoresRetenidosSerializer
)

# Importar serializers de drogas
from .drogas_serializers import (
    # Serializers completos
    PlantillaEnvPBCSerializer, PlantillaEnvCCSerializer, PlantillaEnvMarihuanaSerializer,
    PlantillaKgPBCSerializer, PlantillaKgCCSerializer, PlantillaKgMarihuanaSerializer,
    PlantillaKgLatexOpioSerializer, PlantillaKgDrogaSinteticaSerializer,
    # Serializers para listados
    PlantillaEnvPBCListSerializer, PlantillaEnvCCListSerializer, PlantillaEnvMarihuanaListSerializer,
    PlantillaKgPBCListSerializer, PlantillaKgCCListSerializer, PlantillaKgMarihuanaListSerializer,
    PlantillaKgLatexOpioListSerializer, PlantillaKgDrogaSinteticaListSerializer
)

# Lista de todos los serializers disponibles
__all__ = [
    # Base
    'BaseFormularioSerializer', 'UbicacionMixin', 'UnidadPolicialMixin', 
    'DelitoMixin', 'FormularioValidationMixin',
    'SimpleReferenceSerializer', 'SimpleReferenceWithCodeSerializer', 
    'SimpleReferenceWithSiglaSerializer',
    'ProvinciaFiltradaSerializer', 'DistritoFiltradoSerializer',
    'DelitoGeneralFiltradoSerializer', 'DelitoEspecificoFiltradoSerializer',
    'DelitoSubtipoFiltradoSerializer', 'DireccionEspecializadaFiltradaSerializer',
    'TipoArmaFiltradoSerializer',
    
    # Referencia
    'DepartamentoSerializer', 'ProvinciaSerializer', 'DistritoSerializer',
    'NacionalidadSerializer', 'TipoDocumentoSerializer', 'TipoRequisitoriaSerializer',
    'DelitoFueroSerializer', 'DelitoGeneralSerializer', 'DelitoEspecificoSerializer', 'DelitoSubtipoSerializer',
    'DireccionPolicialSerializer', 'DireccionEspecializadaSerializer', 'DivisionPolicialSerializer',
    'DepartamentoPolicialSerializer', 'UnidadPolicialSerializer',
    'CategoriaArmaSerializer', 'TipoArmaSerializer',
    'SituacionDetenidoSerializer', 'FiscaliaSerializer',
    'ProvinciasPorDepartamentoSerializer', 'DistritosPorProvinciaSerializer',
    'DelitosGeneralesPorFueroSerializer', 'DelitosEspecificosPorGeneralSerializer',
    'DelitosSubtiposPorEspecificoSerializer', 'DireccionesEspecializadasPorDireccionSerializer',
    'TiposArmaPorCategoriaSerializer',
    
    # Personas
    'PlantillaRQSerializer', 'PlantillaDetenidosSerializer', 'PlantillaMenoresRetenidosSerializer',
    
    # Drogas
    'PlantillaEnvPBCSerializer', 'PlantillaEnvCCSerializer', 'PlantillaEnvMarihuanaSerializer',
    'PlantillaKgPBCSerializer', 'PlantillaKgCCSerializer', 'PlantillaKgMarihuanaSerializer',
    'PlantillaKgLatexOpioSerializer', 'PlantillaKgDrogaSinteticaSerializer',
    'PlantillaEnvPBCListSerializer', 'PlantillaEnvCCListSerializer', 'PlantillaEnvMarihuanaListSerializer',
    'PlantillaKgPBCListSerializer', 'PlantillaKgCCListSerializer', 'PlantillaKgMarihuanaListSerializer',
    'PlantillaKgLatexOpioListSerializer', 'PlantillaKgDrogaSinteticaListSerializer',
]
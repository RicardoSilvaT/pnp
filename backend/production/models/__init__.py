# Importar todos los modelos de referencia
from .reference_models import (
    # Ubicación
    Departamento, Provincia, Distrito,
    
    # Personas
    Nacionalidad, TipoDocumento, TipoRequisitoria,
    
    # Delitos
    DelitoFuero, DelitoGeneral, DelitoEspecifico, DelitoSubtipo,
    
    # Estructura Policial
    DireccionPolicial, DireccionEspecializada, DivisionPolicial,
    DepartamentoPolicial, UnidadPolicial,
    
    # Armas
    CategoriaArma, TipoArma,
    
    # Judicial/Procesal
    SituacionDetenido, Fiscalia
)

# Importar modelos base y mixins
from .base_models import (
    BaseFormulario, UbicacionMixin, PersonaBaseMixin, DelitoMixin,
    UnidadPolicialMixin, FuncionarioPublicoMixin, ArmaMixin,
    SituacionProcesalMixin, InformacionFiscalMixin, InformacionAdicionalMixin
)

# Importar modelos de plantillas de personas
from .personas_models import (
    PlantillaRQ, PlantillaDetenidos, PlantillaMenoresRetenidos
)

# Importar modelos de plantillas de drogas
from .drogas_models import (
    PlantillaEnvPBC, PlantillaEnvCC, PlantillaEnvMarihuana,
    PlantillaKgPBC, PlantillaKgCC, PlantillaKgMarihuana,
    PlantillaKgLatexOpio, PlantillaKgDrogaSintetica
)

# Lista de todos los modelos disponibles para importación
__all__ = [
    # Modelos de referencia
    'Departamento', 'Provincia', 'Distrito',
    'Nacionalidad', 'TipoDocumento', 'TipoRequisitoria',
    'DelitoFuero', 'DelitoGeneral', 'DelitoEspecifico', 'DelitoSubtipo',
    'DireccionPolicial', 'DireccionEspecializada', 'DivisionPolicial',
    'DepartamentoPolicial', 'UnidadPolicial',
    'CategoriaArma', 'TipoArma',
    'SituacionDetenido', 'Fiscalia',
    
    # Modelos base
    'BaseFormulario', 'UbicacionMixin', 'PersonaBaseMixin', 'DelitoMixin',
    'UnidadPolicialMixin', 'FuncionarioPublicoMixin', 'ArmaMixin',
    'SituacionProcesalMixin', 'InformacionFiscalMixin', 'InformacionAdicionalMixin',
    
    # Modelos de plantillas
    'PlantillaRQ', 'PlantillaDetenidos', 'PlantillaMenoresRetenidos',
    
    # Modelos de plantillas de drogas
    'PlantillaEnvPBC', 'PlantillaEnvCC', 'PlantillaEnvMarihuana',
    'PlantillaKgPBC', 'PlantillaKgCC', 'PlantillaKgMarihuana',
    'PlantillaKgLatexOpio', 'PlantillaKgDrogaSintetica',
]
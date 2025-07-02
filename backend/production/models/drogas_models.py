from django.db import models
from .base_models import (
    BaseFormulario, UbicacionMixin, UnidadPolicialMixin, InformacionAdicionalMixin
)


# =============================================================================
# CLASE BASE PARA FORMULARIOS DE DROGAS
# =============================================================================

class BaseDrogaFormulario(BaseFormulario, UbicacionMixin, UnidadPolicialMixin, InformacionAdicionalMixin):
    """
    Clase base abstracta para todos los formularios de drogas
    """
    
    # Campos específicos de fecha para drogas (incautación)
    fecha_incautacion = models.DateField(verbose_name="Fecha de Incautación")
    hora_incautacion = models.TimeField(verbose_name="Hora de Incautación")
    
    # Ocultar campos heredados que no se usan en formularios de drogas
    fecha_registro = None
    hora_registro = None
    
    class Meta:
        abstract = True


# =============================================================================
# PLANTILLAS DE ENVOLTORIOS DE DROGAS (3 tablas)
# =============================================================================

class PlantillaEnvPBC(BaseDrogaFormulario):
    """
    Modelo para el formulario de Envoltorios de Pasta Básica de Cocaína
    """
    
    class Meta:
        db_table = 'plantilla_env_pbc'
        verbose_name = 'ENV PBC - Envoltorio de Pasta Básica de Cocaína'
        verbose_name_plural = 'ENV PBC - Envoltorios de Pasta Básica de Cocaína'
        ordering = ['-fecha_incautacion', '-numero_registro']
    
    # Campo específico: cantidad de envoltorios
    cantidad_unidades = models.PositiveIntegerField(
        verbose_name="Cantidad Unidades (Envoltorios PBC)",
        help_text="Número de envoltorios de PBC incautados"
    )
    
    def __str__(self):
        return f"ENV-PBC-{self.numero_registro:03d} - {self.cantidad_unidades} envoltorios - {self.fecha_incautacion}"


class PlantillaEnvCC(BaseDrogaFormulario):
    """
    Modelo para el formulario de Envoltorios de Clorhidrato de Cocaína
    """
    
    class Meta:
        db_table = 'plantilla_env_cc'
        verbose_name = 'ENV CC - Envoltorio de Clorhidrato de Cocaína'
        verbose_name_plural = 'ENV CC - Envoltorios de Clorhidrato de Cocaína'
        ordering = ['-fecha_incautacion', '-numero_registro']
    
    # Campo específico: cantidad de envoltorios
    cantidad_unidades = models.PositiveIntegerField(
        verbose_name="Cantidad Unidades (Envoltorios CC)",
        help_text="Número de envoltorios de CC incautados"
    )
    
    def __str__(self):
        return f"ENV-CC-{self.numero_registro:03d} - {self.cantidad_unidades} envoltorios - {self.fecha_incautacion}"


class PlantillaEnvMarihuana(BaseDrogaFormulario):
    """
    Modelo para el formulario de Envoltorios de Marihuana
    """
    
    class Meta:
        db_table = 'plantilla_env_marihuana'
        verbose_name = 'ENV MARIHUANA - Envoltorio de Marihuana'
        verbose_name_plural = 'ENV MARIHUANA - Envoltorios de Marihuana'
        ordering = ['-fecha_incautacion', '-numero_registro']
    
    # Campo específico: cantidad de envoltorios
    cantidad_unidades = models.PositiveIntegerField(
        verbose_name="Cantidad Unidades (Envoltorios Marihuana)",
        help_text="Número de envoltorios de Marihuana incautados"
    )
    
    def __str__(self):
        return f"ENV-MAR-{self.numero_registro:03d} - {self.cantidad_unidades} envoltorios - {self.fecha_incautacion}"


# =============================================================================
# PLANTILLAS DE KILOGRAMOS DE DROGAS (6 tablas)
# =============================================================================

class PlantillaKgPBC(BaseDrogaFormulario):
    """
    Modelo para el formulario de Kilogramos de Pasta Básica de Cocaína
    """
    
    class Meta:
        db_table = 'plantilla_kg_pbc'
        verbose_name = 'KG PBC - Kilogramos de Pasta Básica de Cocaína'
        verbose_name_plural = 'KG PBC - Kilogramos de Pasta Básica de Cocaína'
        ordering = ['-fecha_incautacion', '-numero_registro']
    
    # Campo específico: peso en kilogramos
    cantidad_kilogramos = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Cantidad Kilogramos (KG PBC)",
        help_text="Peso en kilogramos de PBC incautados"
    )
    
    def __str__(self):
        return f"KG-PBC-{self.numero_registro:03d} - {self.cantidad_kilogramos} kg - {self.fecha_incautacion}"


class PlantillaKgCC(BaseDrogaFormulario):
    """
    Modelo para el formulario de Kilogramos de Clorhidrato de Cocaína
    """
    
    class Meta:
        db_table = 'plantilla_kg_cc'
        verbose_name = 'KG CC - Kilogramos de Clorhidrato de Cocaína'
        verbose_name_plural = 'KG CC - Kilogramos de Clorhidrato de Cocaína'
        ordering = ['-fecha_incautacion', '-numero_registro']
    
    # Campo específico: peso en kilogramos
    cantidad_kilogramos = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Cantidad Kilogramos (KG CC)",
        help_text="Peso en kilogramos de CC incautados"
    )
    
    def __str__(self):
        return f"KG-CC-{self.numero_registro:03d} - {self.cantidad_kilogramos} kg - {self.fecha_incautacion}"


class PlantillaKgMarihuana(BaseDrogaFormulario):
    """
    Modelo para el formulario de Kilogramos de Marihuana
    """
    
    class Meta:
        db_table = 'plantilla_kg_marihuana'
        verbose_name = 'KG MARIHUANA - Kilogramos de Marihuana'
        verbose_name_plural = 'KG MARIHUANA - Kilogramos de Marihuana'
        ordering = ['-fecha_incautacion', '-numero_registro']
    
    # Campo específico: peso en kilogramos
    cantidad_kilogramos = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Cantidad Kilogramos (KG Marihuana)",
        help_text="Peso en kilogramos de Marihuana incautados"
    )
    
    def __str__(self):
        return f"KG-MAR-{self.numero_registro:03d} - {self.cantidad_kilogramos} kg - {self.fecha_incautacion}"


class PlantillaKgLatexOpio(BaseDrogaFormulario):
    """
    Modelo para el formulario de Kilogramos de Látex de Opio
    """
    
    class Meta:
        db_table = 'plantilla_kg_latex_opio'
        verbose_name = 'KG LÁTEX DE OPIO - Kilogramos de Látex de Opio'
        verbose_name_plural = 'KG LÁTEX DE OPIO - Kilogramos de Látex de Opio'
        ordering = ['-fecha_incautacion', '-numero_registro']
    
    # Campo específico: peso en kilogramos
    cantidad_kilogramos = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Cantidad Kilogramos (KG Látex de Opio)",
        help_text="Peso en kilogramos de Látex de Opio incautados"
    )
    
    def __str__(self):
        return f"KG-OPIO-{self.numero_registro:03d} - {self.cantidad_kilogramos} kg - {self.fecha_incautacion}"


class PlantillaKgDrogaSintetica(BaseDrogaFormulario):
    """
    Modelo para el formulario de Kilogramos de Droga Sintética
    """
    
    class Meta:
        db_table = 'plantilla_kg_droga_sintetica'
        verbose_name = 'KG DROGA SINTÉTICA - Kilogramos de Droga Sintética'
        verbose_name_plural = 'KG DROGA SINTÉTICA - Kilogramos de Droga Sintética'
        ordering = ['-fecha_incautacion', '-numero_registro']
    
    # Campo específico: peso en kilogramos
    cantidad_kilogramos = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Cantidad Kilogramos (KG Droga Sintética)",
        help_text="Peso en kilogramos de Droga Sintética incautados"
    )
    
    def __str__(self):
        return f"KG-SINT-{self.numero_registro:03d} - {self.cantidad_kilogramos} kg - {self.fecha_incautacion}"
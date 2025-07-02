from django.db import models
from .base_models import (
    BaseFormulario, UbicacionMixin, PersonaBaseMixin, DelitoMixin,
    UnidadPolicialMixin, FuncionarioPublicoMixin, ArmaMixin,
    SituacionProcesalMixin, InformacionFiscalMixin, InformacionAdicionalMixin
)
from .reference_models import TipoRequisitoria


# =============================================================================
# PLANTILLA RQ: CUADRO DE PERSONAS DETENIDAS POR REQUISITORIAS
# =============================================================================

class PlantillaRQ(
    BaseFormulario,
    PersonaBaseMixin,
    UbicacionMixin,
    FuncionarioPublicoMixin,
    DelitoMixin,
    UnidadPolicialMixin,
    InformacionAdicionalMixin
):
    """
    Modelo para el formulario de Requisitorias (RQ)
    """
    
    # Cambiar nombres de campos base para que coincidan con el formulario
    class Meta:
        db_table = 'plantilla_rq'
        verbose_name = 'RQ - Persona Detenida por Requisitoria'
        verbose_name_plural = 'RQ - Personas Detenidas por Requisitorias'
        ordering = ['-fecha_detencion', '-numero_registro']
    
    # Campos específicos de RQ
    tipo_requisitoria = models.ForeignKey(
        TipoRequisitoria,
        on_delete=models.PROTECT,
        verbose_name="Tipo de Requisitoria"
    )
    
    LISTA_MAS_BUSCADOS_CHOICES = [
        ('SÍ', 'SÍ'),
        ('NO', 'NO'),
    ]
    esta_en_lista_mas_buscados = models.CharField(
        max_length=3,
        choices=LISTA_MAS_BUSCADOS_CHOICES,
        verbose_name="¿Está en lista de más buscados?",
        default='NO'
    )
    
    # Información judicial específica de RQ
    autoridad_que_solicita = models.TextField(
        verbose_name="Autoridad que Solicita",
        null=True,
        blank=True
    )
    
    documento_que_solicita = models.TextField(
        verbose_name="Documento que Solicita", 
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"RQ-{self.numero_registro:03d} - {self.apellido_paterno} {self.apellido_materno}, {self.nombres}"
    
    # Sobrescribir el campo fecha_registro para usar nombres específicos del formulario
    fecha_detencion = models.DateField(verbose_name="Fecha de Detención")
    hora_detencion = models.TimeField(verbose_name="Hora de Detención")
    
    # Ocultar campos heredados que no se usan en este contexto
    fecha_registro = None
    hora_registro = None


# =============================================================================
# PLANTILLA DETENIDOS: CUADRO DE PERSONAS DETENIDAS POR DIVERSOS DELITOS
# =============================================================================

class PlantillaDetenidos(
    BaseFormulario,
    PersonaBaseMixin,
    UbicacionMixin,
    FuncionarioPublicoMixin,
    DelitoMixin,
    UnidadPolicialMixin,
    ArmaMixin,
    SituacionProcesalMixin,
    InformacionFiscalMixin,
    InformacionAdicionalMixin
):
    """
    Modelo para el formulario de Detenidos por Diversos Delitos
    """
    
    class Meta:
        db_table = 'plantilla_detenidos'
        verbose_name = 'Detenido por Diversos Delitos'
        verbose_name_plural = 'Detenidos por Diversos Delitos'
        ordering = ['-fecha_detencion', '-numero_registro']
    
    # Campos específicos de fecha para detenidos
    fecha_detencion = models.DateField(verbose_name="Fecha de Detención")
    hora_detencion = models.TimeField(verbose_name="Hora de Detención")
    
    # Motivo específico de la detención
    MOTIVO_DETENCION_CHOICES = [
        ('FLAGRANCIA', 'FLAGRANCIA'),
        ('DETENCIÓN PRELIMINAR', 'DETENCIÓN PRELIMINAR'),
    ]
    motivo_detencion = models.CharField(
        max_length=50,
        choices=MOTIVO_DETENCION_CHOICES,
        verbose_name="¿Motivo de la detención?"
    )
    
    # Información sobre organizaciones criminales
    BBCC_OOCC_CHOICES = [
        ('SÍ', 'SÍ'),
        ('NO', 'NO'),
    ]
    es_integrante_bbcc_oocc = models.CharField(
        max_length=3,
        choices=BBCC_OOCC_CHOICES,
        verbose_name="¿Es integrante de una BBCC/OOCC?",
        default='NO'
    )
    
    nombre_bbcc_oocc = models.TextField(
        verbose_name="Nombre de la BBCC/OOCC",
        null=True,
        blank=True,
        help_text="Obligatorio solo si es integrante de BBCC/OOCC"
    )
    
    # Segunda unidad policial (Puesto a Disposición)
    direccion_policial_2 = models.ForeignKey(
        'DireccionPolicial',
        on_delete=models.PROTECT,
        verbose_name="PTO A DISP - DIRNIC/DIRNOS 2",
        related_name='detenidos_pto_disp_direccion',
        null=True,
        blank=True
    )
    direccion_especializada_2 = models.ForeignKey(
        'DireccionEspecializada',
        on_delete=models.PROTECT,
        verbose_name="PTO A DISP - Direcciones/Regiones/Frentes 2",
        related_name='detenidos_pto_disp_especializada',
        null=True,
        blank=True
    )
    division_policial_2 = models.ForeignKey(
        'DivisionPolicial',
        on_delete=models.PROTECT,
        verbose_name="PTO A DISP - División Policial 2",
        related_name='detenidos_pto_disp_division',
        null=True,
        blank=True
    )
    departamento_policial_2 = models.ForeignKey(
        'DepartamentoPolicial',
        on_delete=models.PROTECT,
        verbose_name="PTO A DISP - Departamento Policial 2",
        related_name='detenidos_pto_disp_departamento',
        null=True,
        blank=True
    )
    unidad_policial_2 = models.ForeignKey(
        'UnidadPolicial',
        on_delete=models.PROTECT,
        verbose_name="PTO A DISP - Unidad/Área/Equipo 2",
        related_name='detenidos_pto_disp_unidad',
        null=True,
        blank=True
    )
    
    # Información adicional específica de detenidos
    vehiculo_implicado = models.TextField(
        verbose_name="Vehículo Implicado",
        null=True,
        blank=True
    )
    
    # Ocultar campos heredados que no se usan
    fecha_registro = None
    hora_registro = None
    
    def __str__(self):
        return f"DET-{self.numero_registro:03d} - {self.apellido_paterno} {self.apellido_materno}, {self.nombres}"


# =============================================================================
# PLANTILLA MENORES RETENIDOS: CUADRO DE MENORES RETENIDOS POR DIVERSOS DELITOS
# =============================================================================

class PlantillaMenoresRetenidos(
    BaseFormulario,
    PersonaBaseMixin,
    UbicacionMixin,
    DelitoMixin,
    UnidadPolicialMixin,
    ArmaMixin,
    SituacionProcesalMixin,
    InformacionFiscalMixin,
    InformacionAdicionalMixin
):
    """
    Modelo para el formulario de Menores Retenidos por Diversos Delitos
    """
    
    class Meta:
        db_table = 'plantilla_menores_retenidos'
        verbose_name = 'Menor Retenido por Diversos Delitos'
        verbose_name_plural = 'Menores Retenidos por Diversos Delitos'
        ordering = ['-fecha_detencion', '-numero_registro']
    
    # Campos específicos de fecha para menores
    fecha_detencion = models.DateField(verbose_name="Fecha de Detención")
    hora_detencion = models.TimeField(verbose_name="Hora de Detención")
    
    # Motivo específico de la detención
    MOTIVO_DETENCION_CHOICES = [
        ('FLAGRANCIA', 'FLAGRANCIA'),
        ('DETENCIÓN PRELIMINAR', 'DETENCIÓN PRELIMINAR'),
    ]
    motivo_detencion = models.CharField(
        max_length=50,
        choices=MOTIVO_DETENCION_CHOICES,
        verbose_name="¿Motivo de la detención?"
    )
    
    # Información sobre organizaciones criminales
    BBCC_OOCC_CHOICES = [
        ('SÍ', 'SÍ'),
        ('NO', 'NO'),
    ]
    es_integrante_bbcc_oocc = models.CharField(
        max_length=3,
        choices=BBCC_OOCC_CHOICES,
        verbose_name="¿Es integrante de una BBCC/OOCC?",
        default='NO'
    )
    
    nombre_bbcc_oocc = models.TextField(
        verbose_name="Nombre de la BBCC/OOCC",
        null=True,
        blank=True,
        help_text="Obligatorio solo si es integrante de BBCC/OOCC"
    )
    
    # Segunda unidad policial (Puesto a Disposición)
    direccion_policial_2 = models.ForeignKey(
        'DireccionPolicial',
        on_delete=models.PROTECT,
        verbose_name="PTO A DISP - DIRNIC/DIRNOS 2",
        related_name='menores_pto_disp_direccion',
        null=True,
        blank=True
    )
    direccion_especializada_2 = models.ForeignKey(
        'DireccionEspecializada',
        on_delete=models.PROTECT,
        verbose_name="PTO A DISP - Direcciones/Regiones/Frentes 2",
        related_name='menores_pto_disp_especializada',
        null=True,
        blank=True
    )
    division_policial_2 = models.ForeignKey(
        'DivisionPolicial',
        on_delete=models.PROTECT,
        verbose_name="PTO A DISP - División Policial 2",
        related_name='menores_pto_disp_division',
        null=True,
        blank=True
    )
    departamento_policial_2 = models.ForeignKey(
        'DepartamentoPolicial',
        on_delete=models.PROTECT,
        verbose_name="PTO A DISP - Departamento Policial 2",
        related_name='menores_pto_disp_departamento',
        null=True,
        blank=True
    )
    unidad_policial_2 = models.ForeignKey(
        'UnidadPolicial',
        on_delete=models.PROTECT,
        verbose_name="PTO A DISP - Unidad/Área/Equipo 2",
        related_name='menores_pto_disp_unidad',
        null=True,
        blank=True
    )
    
    # Ocultar campos heredados que no se usan
    fecha_registro = None
    hora_registro = None
    
    def __str__(self):
        return f"MEN-{self.numero_registro:03d} - {self.apellido_paterno} {self.apellido_materno}, {self.nombres}"
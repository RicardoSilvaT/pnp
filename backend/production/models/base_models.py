from django.db import models
from django.contrib.auth import get_user_model
from .reference_models import (
    Departamento, Provincia, Distrito, Nacionalidad, TipoDocumento,
    DelitoFuero, DelitoGeneral, DelitoEspecifico, DelitoSubtipo,
    DireccionPolicial, DireccionEspecializada, DivisionPolicial, 
    DepartamentoPolicial, UnidadPolicial, CategoriaArma, TipoArma,
    SituacionDetenido, Fiscalia, TipoRequisitoria
)

User = get_user_model()


# =============================================================================
# CLASE BASE ABSTRACTA PARA TODOS LOS FORMULARIOS
# =============================================================================

class BaseFormulario(models.Model):
    """
    Clase base abstracta que contiene campos comunes a todos los formularios
    """
    numero_registro = models.PositiveIntegerField(
        verbose_name="N° Registro",
        help_text="Número de registro autoincremental por tipo de plantilla"
    )
    
    # Campos de fecha y hora
    fecha_registro = models.DateField(
        verbose_name="Fecha de Registro",
        help_text="Fecha en que se registra el evento"
    )
    hora_registro = models.TimeField(
        verbose_name="Hora de Registro", 
        help_text="Hora en que se registra el evento"
    )
    
    # Metadatos del sistema
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creado el"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Actualizado el"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
        verbose_name="Creado por"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated",
        verbose_name="Actualizado por"
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


# =============================================================================
# MIXINS REUTILIZABLES
# =============================================================================

class UbicacionMixin(models.Model):
    """
    Mixin para campos de ubicación geográfica con filtros cascada
    """
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.PROTECT,
        verbose_name="Departamento"
    )
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.PROTECT,
        verbose_name="Provincia"
    )
    distrito = models.ForeignKey(
        Distrito,
        on_delete=models.PROTECT,
        verbose_name="Distrito"
    )
    
    class Meta:
        abstract = True


class PersonaBaseMixin(models.Model):
    """
    Mixin para datos básicos de una persona
    """
    apellido_paterno = models.CharField(
        max_length=100,
        verbose_name="Apellido Paterno"
    )
    apellido_materno = models.CharField(
        max_length=100,
        verbose_name="Apellido Materno"
    )
    nombres = models.CharField(
        max_length=100,
        verbose_name="Nombres"
    )
    edad = models.PositiveSmallIntegerField(
        verbose_name="Edad",
        help_text="Edad de la persona (0-120 años)"
    )
    
    GENERO_CHOICES = [
        ('MASCULINO', 'MASCULINO'),
        ('FEMENINO', 'FEMENINO'),
    ]
    genero = models.CharField(
        max_length=20,
        choices=GENERO_CHOICES,
        verbose_name="Género"
    )
    
    nacionalidad = models.ForeignKey(
        Nacionalidad,
        on_delete=models.PROTECT,
        verbose_name="Nacionalidad"
    )
    tipo_documento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        verbose_name="Tipo de Documento"
    )
    numero_documento = models.CharField(
        max_length=20,
        verbose_name="N° Documento",
        help_text="Preserva ceros iniciales"
    )
    
    class Meta:
        abstract = True


class DelitoMixin(models.Model):
    """
    Mixin para información de delitos (principal y secundario)
    """
    # DELITO PRINCIPAL
    TENTATIVA_CHOICES = [
        ('SÍ', 'SÍ'),
        ('NO', 'NO'),
    ]
    
    es_tentativa = models.CharField(
        max_length=3,
        choices=TENTATIVA_CHOICES,
        verbose_name="¿Es tentativa?",
        default='NO'
    )
    
    delito_fuero = models.ForeignKey(
        DelitoFuero,
        on_delete=models.PROTECT,
        verbose_name="Fuero/Leyes Especiales"
    )
    delito_general = models.ForeignKey(
        DelitoGeneral,
        on_delete=models.PROTECT,
        verbose_name="Delito General"
    )
    delito_especifico = models.ForeignKey(
        DelitoEspecifico,
        on_delete=models.PROTECT,
        verbose_name="Delito Específico"
    )
    delito_subtipo = models.ForeignKey(
        DelitoSubtipo,
        on_delete=models.PROTECT,
        verbose_name="Sub Tipo"
    )
    
    # DELITO SECUNDARIO (opcional)
    es_tentativa_2 = models.CharField(
        max_length=3,
        choices=TENTATIVA_CHOICES,
        verbose_name="¿Es tentativa 2?",
        null=True,
        blank=True
    )
    
    delito_fuero_2 = models.ForeignKey(
        DelitoFuero,
        on_delete=models.PROTECT,
        verbose_name="Fuero/Leyes Especiales 2",
        related_name="%(app_label)s_%(class)s_fuero2",
        null=True,
        blank=True
    )
    delito_general_2 = models.ForeignKey(
        DelitoGeneral,
        on_delete=models.PROTECT,
        verbose_name="Delito General 2",
        related_name="%(app_label)s_%(class)s_general2",
        null=True,
        blank=True
    )
    delito_especifico_2 = models.ForeignKey(
        DelitoEspecifico,
        on_delete=models.PROTECT,
        verbose_name="Delito Específico 2",
        related_name="%(app_label)s_%(class)s_especifico2",
        null=True,
        blank=True
    )
    delito_subtipo_2 = models.ForeignKey(
        DelitoSubtipo,
        on_delete=models.PROTECT,
        verbose_name="Sub Tipo 2",
        related_name="%(app_label)s_%(class)s_subtipo2",
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True


class UnidadPolicialMixin(models.Model):
    """
    Mixin para información de la unidad policial
    """
    direccion_policial = models.ForeignKey(
        DireccionPolicial,
        on_delete=models.PROTECT,
        verbose_name="Dirección - DIRNIC/DIRNOS"
    )
    direccion_especializada = models.ForeignKey(
        DireccionEspecializada,
        on_delete=models.PROTECT,
        verbose_name="Dirección Especializada/Región/Frente",
        null=True,
        blank=True
    )
    division_policial = models.ForeignKey(
        DivisionPolicial,
        on_delete=models.PROTECT,
        verbose_name="División Policial",
        null=True,
        blank=True
    )
    departamento_policial = models.ForeignKey(
        DepartamentoPolicial,
        on_delete=models.PROTECT,
        verbose_name="Departamento Policial",
        null=True,
        blank=True
    )
    unidad_policial = models.ForeignKey(
        UnidadPolicial,
        on_delete=models.PROTECT,
        verbose_name="Unidad/Área/Equipo",
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True


class FuncionarioPublicoMixin(models.Model):
    """
    Mixin para información sobre funcionarios públicos
    """
    FUNCIONARIO_CHOICES = [
        ('PARTICULARES', 'PARTICULARES'),
        ('FUNCIONARIO PUBLICO', 'FUNCIONARIO PUBLICO'),
        ('SERVIDOR PUBLICO', 'SERVIDOR PUBLICO'),
        ('EX FUNCIONARIO PUBLICO', 'EX FUNCIONARIO PUBLICO'),
        ('EX SERVIDOR PUBLICO', 'EX SERVIDOR PUBLICO'),
    ]
    
    es_funcionario_publico = models.CharField(
        max_length=50,
        choices=FUNCIONARIO_CHOICES,
        verbose_name="¿Es funcionario público?",
        default='PARTICULARES'
    )
    
    entidad_publica = models.TextField(
        verbose_name="Entidad Pública",
        null=True,
        blank=True,
        help_text="Solo si NO es PARTICULARES"
    )
    
    detalle_entidad = models.TextField(
        verbose_name="Detalle de Entidad",
        null=True,
        blank=True,
        help_text="Solo si NO es PARTICULARES"
    )
    
    class Meta:
        abstract = True


class ArmaMixin(models.Model):
    """
    Mixin para información de armas
    """
    categoria_arma = models.ForeignKey(
        CategoriaArma,
        on_delete=models.PROTECT,
        verbose_name="Tipo de Arma",
        null=True,
        blank=True
    )
    tipo_arma = models.ForeignKey(
        TipoArma,
        on_delete=models.PROTECT,
        verbose_name="Especificación del Arma",
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True


class SituacionProcesalMixin(models.Model):
    """
    Mixin para situación procesal del detenido
    """
    situacion_detenido = models.ForeignKey(
        SituacionDetenido,
        on_delete=models.PROTECT,
        verbose_name="Situación Actual del Detenido",
        null=True,
        blank=True
    )
    
    documento_libertad = models.TextField(
        verbose_name="Documento de Libertad",
        null=True,
        blank=True,
        help_text="Documento con el que le dieron libertad"
    )
    
    documento_disposicion = models.TextField(
        verbose_name="Documento de Disposición",
        null=True,
        blank=True,
        help_text="Documento con el que se pone a disposición"
    )
    
    class Meta:
        abstract = True


class InformacionFiscalMixin(models.Model):
    """
    Mixin para información fiscal
    """
    nombre_fiscal = models.TextField(
        verbose_name="Nombre del Fiscal a Cargo",
        null=True,
        blank=True
    )
    
    fiscalia = models.ForeignKey(
        Fiscalia,
        on_delete=models.PROTECT,
        verbose_name="Fiscalía",
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True


class InformacionAdicionalMixin(models.Model):
    """
    Mixin para campos adicionales comunes
    """
    TIPO_INTERVENCION_CHOICES = [
        ('OPERATIVO', 'OPERATIVO'),
        ('INTERVENCIÓN', 'INTERVENCIÓN'),
    ]
    
    nota_informativa_sicpip = models.TextField(
        verbose_name="Nota Informativa SICPIP",
        null=True,
        blank=True
    )
    
    tipo_intervencion = models.CharField(
        max_length=50,
        choices=TIPO_INTERVENCION_CHOICES,
        verbose_name="Tipo Intervención",
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True
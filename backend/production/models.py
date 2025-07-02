from django.db import models
from django.conf import settings


# ======================================
# TABLAS DE CONFIGURACIÓN
# ======================================


class Plantilla(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        db_table = 'plantilla'
        verbose_name = 'Plantilla'
        verbose_name_plural = 'Plantillas'
   
    def __str__(self):
        return self.nombre


class CampoPlantilla(models.Model):
    TIPOS_CAMPO = [
        ('text', 'Texto'),
        ('number', 'Número'),
        ('date', 'Fecha'),
        ('time', 'Hora'),
        ('select', 'Lista desplegable'),
        ('textarea', 'Área de texto'),
        ('checkbox', 'Casilla de verificación'),
    ]
   
    plantilla = models.ForeignKey(Plantilla, on_delete=models.CASCADE, related_name='campos')
    nombre_campo = models.CharField(max_length=100)
    etiqueta_campo = models.CharField(max_length=200)
    tipo_campo = models.CharField(max_length=20, choices=TIPOS_CAMPO)
    requerido = models.BooleanField(default=False)
    orden_campo = models.PositiveIntegerField()
    opciones = models.JSONField(blank=True, null=True)
    grupo_campo = models.CharField(max_length=100, blank=True, null=True)
   
    class Meta:
        db_table = 'campo_plantilla'
        verbose_name = 'Campo de Plantilla'
        verbose_name_plural = 'Campos de Plantilla'
        ordering = ['orden_campo']
   
    def __str__(self):
        return f"{self.plantilla.nombre} - {self.etiqueta_campo}"


# ======================================
# TABLAS DE CATÁLOGOS
# ======================================


class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, unique=True)
   
    class Meta:
        db_table = 'departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre']
   
    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='provincias')
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
   
    class Meta:
        db_table = 'provincia'
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['nombre']
        unique_together = ['departamento', 'codigo']
   
    def __str__(self):
        return f"{self.nombre} - {self.departamento.nombre}"


class Distrito(models.Model):
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='distritos')
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
   
    class Meta:
        db_table = 'distrito'
        verbose_name = 'Distrito'
        verbose_name_plural = 'Distritos'
        ordering = ['nombre']
        unique_together = ['provincia', 'codigo']
   
    def __str__(self):
        return f"{self.nombre} - {self.provincia.nombre}"


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    codigo = models.CharField(max_length=10, unique=True)
   
    class Meta:
        db_table = 'tipo_documento'
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documento'
        ordering = ['nombre']
   
    def __str__(self):
        return self.nombre


class DelitoGeneral(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    codigo = models.CharField(max_length=20, unique=True)
   
    class Meta:
        db_table = 'delito_general'
        verbose_name = 'Delito General'
        verbose_name_plural = 'Delitos Generales'
        ordering = ['nombre']
   
    def __str__(self):
        return self.nombre


class DelitoEspecifico(models.Model):
    delito_general = models.ForeignKey(DelitoGeneral, on_delete=models.CASCADE, related_name='delitos_especificos')
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20)
   
    class Meta:
        db_table = 'delito_especifico'
        verbose_name = 'Delito Específico'
        verbose_name_plural = 'Delitos Específicos'
        ordering = ['nombre']
        unique_together = ['delito_general', 'codigo']
   
    def __str__(self):
        return f"{self.nombre} ({self.delito_general.nombre})"


class SubTipoDelito(models.Model):
    delito_especifico = models.ForeignKey(DelitoEspecifico, on_delete=models.CASCADE, related_name='sub_tipos')
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20)
   
    class Meta:
        db_table = 'sub_tipo_delito'
        verbose_name = 'Sub Tipo de Delito'
        verbose_name_plural = 'Sub Tipos de Delito'
        ordering = ['nombre']
        unique_together = ['delito_especifico', 'codigo']
   
    def __str__(self):
        return f"{self.nombre} ({self.delito_especifico.nombre})"


# ======================================
# TABLA PRINCIPAL DE FORMULARIOS
# ======================================


class SubmisionFormulario(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('enviado', 'Enviado'),
        ('revisado', 'Revisado'),
        ('aprobado', 'Aprobado'),
    ]
   
    plantilla = models.ForeignKey(Plantilla, on_delete=models.CASCADE, related_name='submisiones')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='formularios')
    numero_formulario = models.CharField(max_length=50, unique=True)
    fecha_detencion = models.DateField()
    hora_detencion = models.TimeField()
    nota_informativa_sicpip = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
   
    class Meta:
        db_table = 'submision_formulario'
        verbose_name = 'Submisión de Formulario'
        verbose_name_plural = 'Submisiones de Formulario'
        ordering = ['-fecha_creacion']
   
    def __str__(self):
        return f"{self.numero_formulario} - {self.plantilla.nombre}"


# ======================================
# DATOS NORMALIZADOS POR SECCIONES
# ======================================


class DatosDetenido(models.Model):
    GENEROS = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
   
    submision_formulario = models.OneToOneField(SubmisionFormulario, on_delete=models.CASCADE, related_name='datos_detenido')
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    nombres = models.CharField(max_length=150)
    edad = models.PositiveIntegerField()
    genero = models.CharField(max_length=1, choices=GENEROS)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    numero_documento = models.CharField(max_length=20)
    nacionalidad = models.CharField(max_length=100, default='Peruana')
   
    class Meta:
        db_table = 'datos_detenido'
        verbose_name = 'Datos del Detenido'
        verbose_name_plural = 'Datos de Detenidos'
   
    def __str__(self):
        return f"{self.apellido_paterno} {self.apellido_materno}, {self.nombres}"


class LugarDetencion(models.Model):
    submision_formulario = models.OneToOneField(SubmisionFormulario, on_delete=models.CASCADE, related_name='lugar_detencion')
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
   
    class Meta:
        db_table = 'lugar_detencion'
        verbose_name = 'Lugar de Detención'
        verbose_name_plural = 'Lugares de Detención'
   
    def __str__(self):
        return f"{self.distrito.nombre} - {self.distrito.provincia.nombre}"


class DatosDelito(models.Model):
    submision_formulario = models.ForeignKey(SubmisionFormulario, on_delete=models.CASCADE, related_name='datos_delito')
    sub_tipo_delito = models.ForeignKey(SubTipoDelito, on_delete=models.CASCADE)
    multiples_delitos = models.BooleanField(default=False)
    otros_delitos = models.TextField(blank=True, null=True)
   
    class Meta:
        db_table = 'datos_delito'
        verbose_name = 'Datos del Delito'
        verbose_name_plural = 'Datos de Delitos'
   
    def __str__(self):
        return f"{self.sub_tipo_delito.nombre}"


class DatosUnidad(models.Model):
    submision_formulario = models.OneToOneField(SubmisionFormulario, on_delete=models.CASCADE, related_name='datos_unidad')
    direccion_especializada = models.CharField(max_length=200)
    division_policial = models.CharField(max_length=200)
    departamento_policial = models.CharField(max_length=200)
    nombre_unidad = models.CharField(max_length=200)
   
    class Meta:
        db_table = 'datos_unidad'
        verbose_name = 'Datos de la Unidad'
        verbose_name_plural = 'Datos de Unidades'
   
    def __str__(self):
        return f"{self.nombre_unidad} - {self.division_policial}"


# ======================================
# DATOS ESPECÍFICOS POR PLANTILLA
# ======================================


class DatosRequisitoria(models.Model):
    submision_formulario = models.OneToOneField(SubmisionFormulario, on_delete=models.CASCADE, related_name='datos_requisitoria')
    autoridad_orden_captura = models.CharField(max_length=200)
    pertenece_mas_buscados = models.BooleanField(default=False)
   
    class Meta:
        db_table = 'datos_requisitoria'
        verbose_name = 'Datos de Requisitoria'
        verbose_name_plural = 'Datos de Requisitorias'
   
    def __str__(self):
        return f"RQ - {self.autoridad_orden_captura}"


class DatosDetencion(models.Model):
    MOTIVOS_DETENCION = [
        ('flagrancia', 'Flagrancia'),
        ('detencion_preliminar', 'Detención Preliminar'),
    ]
   
    submision_formulario = models.OneToOneField(SubmisionFormulario, on_delete=models.CASCADE, related_name='datos_detencion')
    motivo_detencion = models.CharField(max_length=30, choices=MOTIVOS_DETENCION)
   
    class Meta:
        db_table = 'datos_detencion'
        verbose_name = 'Datos de Detención'
        verbose_name_plural = 'Datos de Detenciones'
   
    def __str__(self):
        return f"{self.motivo_detencion}"


from django.db import models


# =============================================================================
# TABLAS DE UBICACIÓN GEOGRÁFICA (3 tablas)
# =============================================================================

class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, unique=True, null=True, blank=True)
    
    class Meta:
        db_table = 'departamentos'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='provincias')
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, null=True, blank=True)
    
    class Meta:
        db_table = 'provincias'
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['departamento', 'nombre']
        unique_together = ['departamento', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.departamento.nombre})"


class Distrito(models.Model):
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='distritos')
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, null=True, blank=True)
    
    class Meta:
        db_table = 'distritos'
        verbose_name = 'Distrito'
        verbose_name_plural = 'Distritos'
        ordering = ['provincia', 'nombre']
        unique_together = ['provincia', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.provincia.nombre})"


# =============================================================================
# TABLAS DE PERSONAS (3 tablas)
# =============================================================================

class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, unique=True, null=True, blank=True)
    
    class Meta:
        db_table = 'nacionalidades'
        verbose_name = 'Nacionalidad'
        verbose_name_plural = 'Nacionalidades'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, unique=True, null=True, blank=True)
    
    class Meta:
        db_table = 'tipos_documento'
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documento'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class TipoRequisitoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'tipos_requisitoria'
        verbose_name = 'Tipo de Requisitoria'
        verbose_name_plural = 'Tipos de Requisitoria'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


# =============================================================================
# TABLAS DE DELITOS - ESTRUCTURA JERÁRQUICA (4 tablas)
# =============================================================================

class DelitoFuero(models.Model):
    nombre = models.TextField(unique=True)
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'delito_fuero'
        verbose_name = 'Delito Fuero/Leyes Especiales'
        verbose_name_plural = 'Delitos Fuero/Leyes Especiales'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class DelitoGeneral(models.Model):
    delito_fuero = models.ForeignKey(DelitoFuero, on_delete=models.CASCADE, related_name='delitos_generales')
    nombre = models.TextField()
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'delito_general'
        verbose_name = 'Delito General'
        verbose_name_plural = 'Delitos Generales'
        ordering = ['delito_fuero', 'nombre']
        unique_together = ['delito_fuero', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.delito_fuero.nombre})"


class DelitoEspecifico(models.Model):
    delito_general = models.ForeignKey(DelitoGeneral, on_delete=models.CASCADE, related_name='delitos_especificos')
    nombre = models.TextField()
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'delito_especifico'
        verbose_name = 'Delito Específico'
        verbose_name_plural = 'Delitos Específicos'
        ordering = ['delito_general', 'nombre']
        unique_together = ['delito_general', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.delito_general.nombre})"


class DelitoSubtipo(models.Model):
    delito_especifico = models.ForeignKey(DelitoEspecifico, on_delete=models.CASCADE, related_name='delitos_subtipos')
    nombre = models.TextField()
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'delito_subtipo'
        verbose_name = 'Delito Subtipo'
        verbose_name_plural = 'Delitos Subtipos'
        ordering = ['delito_especifico', 'nombre']
        unique_together = ['delito_especifico', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.delito_especifico.nombre})"


# =============================================================================
# TABLAS DE ESTRUCTURA POLICIAL (5 tablas)
# =============================================================================

class DireccionPolicial(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    sigla = models.CharField(max_length=20, unique=True, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'direcciones_policiales'
        verbose_name = 'Dirección Policial'
        verbose_name_plural = 'Direcciones Policiales'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.sigla} - {self.nombre}" if self.sigla else self.nombre


class DireccionEspecializada(models.Model):
    direccion_policial = models.ForeignKey(DireccionPolicial, on_delete=models.CASCADE, related_name='direcciones_especializadas')
    nombre = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'direcciones_especializadas'
        verbose_name = 'Dirección Especializada/Región/Frente'
        verbose_name_plural = 'Direcciones Especializadas/Regiones/Frentes'
        ordering = ['direccion_policial', 'nombre']
        unique_together = ['direccion_policial', 'nombre']
    
    def __str__(self):
        return f"{self.sigla} - {self.nombre}" if self.sigla else self.nombre


class DivisionPolicial(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    sigla = models.CharField(max_length=20, unique=True, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'divisiones_policiales'
        verbose_name = 'División Policial'
        verbose_name_plural = 'Divisiones Policiales'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.sigla} - {self.nombre}" if self.sigla else self.nombre


class DepartamentoPolicial(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    sigla = models.CharField(max_length=20, unique=True, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'departamentos_policiales'
        verbose_name = 'Departamento Policial'
        verbose_name_plural = 'Departamentos Policiales'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.sigla} - {self.nombre}" if self.sigla else self.nombre


class UnidadPolicial(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    sigla = models.CharField(max_length=20, unique=True, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'unidades_policiales'
        verbose_name = 'Unidad/Área/Equipo Policial'
        verbose_name_plural = 'Unidades/Áreas/Equipos Policiales'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.sigla} - {self.nombre}" if self.sigla else self.nombre


# =============================================================================
# TABLAS DE ARMAS (2 tablas)
# =============================================================================

class CategoriaArma(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'categorias_armas'
        verbose_name = 'Categoría de Arma'
        verbose_name_plural = 'Categorías de Armas'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class TipoArma(models.Model):
    categoria_arma = models.ForeignKey(CategoriaArma, on_delete=models.CASCADE, related_name='tipos_armas')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'tipos_armas'
        verbose_name = 'Tipo de Arma'
        verbose_name_plural = 'Tipos de Armas'
        ordering = ['categoria_arma', 'nombre']
        unique_together = ['categoria_arma', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.categoria_arma.nombre})"


# =============================================================================
# TABLAS JUDICIALES/PROCESALES (2 tablas)
# =============================================================================

class SituacionDetenido(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'situaciones_detenido'
        verbose_name = 'Situación del Detenido'
        verbose_name_plural = 'Situaciones del Detenido'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Fiscalia(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    direccion = models.TextField(null=True, blank=True)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, related_name='fiscalias')
    
    class Meta:
        db_table = 'fiscalias'
        verbose_name = 'Fiscalía'
        verbose_name_plural = 'Fiscalías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
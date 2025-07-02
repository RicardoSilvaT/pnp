from django.contrib import admin
from .models import (
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
    # Judicial
    SituacionDetenido, Fiscalia,
    # Plantillas
    PlantillaRQ, PlantillaDetenidos, PlantillaMenoresRetenidos,
    # Plantillas de drogas
    PlantillaEnvPBC, PlantillaEnvCC, PlantillaEnvMarihuana,
    PlantillaKgPBC, PlantillaKgCC, PlantillaKgMarihuana,
    PlantillaKgLatexOpio, PlantillaKgDrogaSintetica
)


# =============================================================================
# UBICACIÓN GEOGRÁFICA
# =============================================================================

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo']
    search_fields = ['nombre']
    ordering = ['nombre']


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'departamento', 'codigo']
    list_filter = ['departamento']
    search_fields = ['nombre', 'departamento__nombre']
    ordering = ['departamento', 'nombre']


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'provincia', 'get_departamento', 'codigo']
    list_filter = ['provincia__departamento', 'provincia']
    search_fields = ['nombre', 'provincia__nombre', 'provincia__departamento__nombre']
    ordering = ['provincia__departamento', 'provincia', 'nombre']
    
    def get_departamento(self, obj):
        return obj.provincia.departamento.nombre
    get_departamento.short_description = 'Departamento'


# =============================================================================
# DATOS DE PERSONAS
# =============================================================================

@admin.register(Nacionalidad)
class NacionalidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo']
    search_fields = ['nombre']
    ordering = ['nombre']


@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo']
    search_fields = ['nombre']
    ordering = ['nombre']


@admin.register(TipoRequisitoria)
class TipoRequisitoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']
    ordering = ['nombre']


# =============================================================================
# DELITOS
# =============================================================================

@admin.register(DelitoFuero)
class DelitoFueroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']
    ordering = ['nombre']


@admin.register(DelitoGeneral)
class DelitoGeneralAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'delito_fuero', 'descripcion']
    list_filter = ['delito_fuero']
    search_fields = ['nombre', 'delito_fuero__nombre']
    ordering = ['delito_fuero', 'nombre']


@admin.register(DelitoEspecifico)
class DelitoEspecificoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'delito_general', 'get_fuero', 'descripcion']
    list_filter = ['delito_general__delito_fuero', 'delito_general']
    search_fields = ['nombre', 'delito_general__nombre', 'delito_general__delito_fuero__nombre']
    ordering = ['delito_general__delito_fuero', 'delito_general', 'nombre']
    
    def get_fuero(self, obj):
        return obj.delito_general.delito_fuero.nombre
    get_fuero.short_description = 'Fuero'


@admin.register(DelitoSubtipo)
class DelitoSubtipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'delito_especifico', 'get_general', 'get_fuero']
    list_filter = ['delito_especifico__delito_general__delito_fuero', 'delito_especifico__delito_general']
    search_fields = ['nombre', 'delito_especifico__nombre', 'delito_especifico__delito_general__nombre']
    ordering = ['delito_especifico__delito_general__delito_fuero', 'delito_especifico__delito_general', 'delito_especifico', 'nombre']
    
    def get_general(self, obj):
        return obj.delito_especifico.delito_general.nombre
    get_general.short_description = 'Delito General'
    
    def get_fuero(self, obj):
        return obj.delito_especifico.delito_general.delito_fuero.nombre
    get_fuero.short_description = 'Fuero'


# =============================================================================
# ESTRUCTURA POLICIAL
# =============================================================================

@admin.register(DireccionPolicial)
class DireccionPolicialAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nombre', 'descripcion']
    search_fields = ['nombre', 'sigla']
    ordering = ['sigla']


@admin.register(DireccionEspecializada)
class DireccionEspecializadaAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nombre', 'direccion_policial', 'descripcion']
    list_filter = ['direccion_policial']
    search_fields = ['nombre', 'sigla', 'direccion_policial__nombre']
    ordering = ['direccion_policial', 'sigla']


@admin.register(DivisionPolicial)
class DivisionPolicialAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nombre', 'descripcion']
    search_fields = ['nombre', 'sigla']
    ordering = ['sigla']


@admin.register(DepartamentoPolicial)
class DepartamentoPolicialAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nombre', 'descripcion']
    search_fields = ['nombre', 'sigla']
    ordering = ['sigla']


@admin.register(UnidadPolicial)
class UnidadPolicialAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nombre', 'descripcion']
    search_fields = ['nombre', 'sigla']
    ordering = ['nombre']


# =============================================================================
# ARMAS
# =============================================================================

@admin.register(CategoriaArma)
class CategoriaArmaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']
    ordering = ['nombre']


@admin.register(TipoArma)
class TipoArmaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria_arma', 'descripcion']
    list_filter = ['categoria_arma']
    search_fields = ['nombre', 'categoria_arma__nombre']
    ordering = ['categoria_arma', 'nombre']


# =============================================================================
# DATOS JUDICIALES
# =============================================================================

@admin.register(SituacionDetenido)
class SituacionDetenidoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']
    ordering = ['nombre']


@admin.register(Fiscalia)
class FiscaliaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'departamento', 'telefono']
    list_filter = ['departamento']
    search_fields = ['nombre', 'departamento__nombre']
    ordering = ['departamento', 'nombre']


# =============================================================================
# FORMULARIOS/PLANTILLAS
# =============================================================================

class BaseFormularioAdmin(admin.ModelAdmin):
    """Clase base para administrar formularios"""
    date_hierarchy = 'fecha_detencion'
    list_per_page = 25
    
    # Campos de solo lectura
    readonly_fields = ['numero_registro', 'created_at', 'updated_at', 'created_by', 'updated_by']
    
    # Método para guardar con usuario
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.created_by = request.user
            # Auto-generar número de registro
            last_obj = obj.__class__.objects.filter().order_by('-numero_registro').first()
            obj.numero_registro = (last_obj.numero_registro + 1) if last_obj else 1
        else:  # Si es una actualización
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PlantillaRQ)
class PlantillaRQAdmin(BaseFormularioAdmin):
    list_display = [
        'numero_registro', 'fecha_detencion', 'apellido_paterno', 
        'apellido_materno', 'nombres', 'edad', 'genero', 
        'tipo_requisitoria', 'esta_en_lista_mas_buscados'
    ]
    list_filter = [
        'fecha_detencion', 'genero', 'tipo_requisitoria', 
        'esta_en_lista_mas_buscados', 'es_funcionario_publico',
        'departamento', 'nacionalidad'
    ]
    search_fields = [
        'apellido_paterno', 'apellido_materno', 'nombres', 
        'numero_documento', 'autoridad_que_solicita'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_registro', 'fecha_detencion', 'hora_detencion')
        }),
        ('Datos de la Persona', {
            'fields': ('apellido_paterno', 'apellido_materno', 'nombres', 'edad', 'genero',
                      'nacionalidad', 'tipo_documento', 'numero_documento')
        }),
        ('Ubicación de Detención', {
            'fields': ('departamento', 'provincia', 'distrito')
        }),
        ('Información de Requisitoria', {
            'fields': ('tipo_requisitoria', 'esta_en_lista_mas_buscados')
        }),
        ('Información Laboral', {
            'fields': ('es_funcionario_publico', 'entidad_publica', 'detalle_entidad')
        }),
        ('Delito Principal', {
            'fields': ('es_tentativa', 'delito_fuero', 'delito_general', 'delito_especifico', 'delito_subtipo')
        }),
        ('Delito Secundario (Opcional)', {
            'fields': ('es_tentativa_2', 'delito_fuero_2', 'delito_general_2', 'delito_especifico_2', 'delito_subtipo_2'),
            'classes': ['collapse']
        }),
        ('Unidad Policial', {
            'fields': ('direccion_policial', 'direccion_especializada', 'division_policial', 
                      'departamento_policial', 'unidad_policial')
        }),
        ('Información Judicial', {
            'fields': ('autoridad_que_solicita', 'documento_que_solicita')
        }),
        ('Información Adicional', {
            'fields': ('nota_informativa_sicpip', 'tipo_intervencion')
        }),
        ('Metadatos del Sistema', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ['collapse']
        }),
    )


# =============================================================================
# FORMULARIOS DE DROGAS
# =============================================================================

class BaseDrogaAdmin(admin.ModelAdmin):
    """Clase base para administrar formularios de drogas"""
    date_hierarchy = 'fecha_incautacion'
    list_per_page = 25
    
    # Campos de solo lectura
    readonly_fields = ['numero_registro', 'created_at', 'updated_at', 'created_by', 'updated_by']
    
    # Método para guardar con usuario
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.created_by = request.user
            # Auto-generar número de registro
            last_obj = obj.__class__.objects.filter().order_by('-numero_registro').first()
            obj.numero_registro = (last_obj.numero_registro + 1) if last_obj else 1
        else:  # Si es una actualización
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# ENVOLTORIOS DE DROGAS

@admin.register(PlantillaEnvPBC)
class PlantillaEnvPBCAdmin(BaseDrogaAdmin):
    list_display = [
        'numero_registro', 'fecha_incautacion', 'cantidad_unidades', 
        'departamento', 'provincia', 'distrito', 'direccion_policial'
    ]
    list_filter = [
        'fecha_incautacion', 'departamento', 'direccion_policial', 'tipo_intervencion'
    ]
    search_fields = [
        'numero_registro', 'nota_informativa_sicpip', 'departamento__nombre'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_registro', 'fecha_incautacion', 'hora_incautacion')
        }),
        ('Cantidad Incautada', {
            'fields': ('cantidad_unidades',)
        }),
        ('Lugar de Incautación', {
            'fields': ('departamento', 'provincia', 'distrito')
        }),
        ('Unidad Policial', {
            'fields': ('direccion_policial', 'direccion_especializada', 'division_policial', 
                      'departamento_policial', 'unidad_policial')
        }),
        ('Información Adicional', {
            'fields': ('nota_informativa_sicpip', 'tipo_intervencion')
        }),
        ('Metadatos del Sistema', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ['collapse']
        }),
    )


@admin.register(PlantillaEnvCC)
class PlantillaEnvCCAdmin(BaseDrogaAdmin):
    list_display = [
        'numero_registro', 'fecha_incautacion', 'cantidad_unidades', 
        'departamento', 'provincia', 'distrito', 'direccion_policial'
    ]
    list_filter = [
        'fecha_incautacion', 'departamento', 'direccion_policial', 'tipo_intervencion'
    ]
    search_fields = [
        'numero_registro', 'nota_informativa_sicpip', 'departamento__nombre'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_registro', 'fecha_incautacion', 'hora_incautacion')
        }),
        ('Cantidad Incautada', {
            'fields': ('cantidad_unidades',)
        }),
        ('Lugar de Incautación', {
            'fields': ('departamento', 'provincia', 'distrito')
        }),
        ('Unidad Policial', {
            'fields': ('direccion_policial', 'direccion_especializada', 'division_policial', 
                      'departamento_policial', 'unidad_policial')
        }),
        ('Información Adicional', {
            'fields': ('nota_informativa_sicpip', 'tipo_intervencion')
        }),
        ('Metadatos del Sistema', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ['collapse']
        }),
    )


@admin.register(PlantillaEnvMarihuana)
class PlantillaEnvMarihuanaAdmin(BaseDrogaAdmin):
    list_display = [
        'numero_registro', 'fecha_incautacion', 'cantidad_unidades', 
        'departamento', 'provincia', 'distrito', 'direccion_policial'
    ]
    list_filter = [
        'fecha_incautacion', 'departamento', 'direccion_policial', 'tipo_intervencion'
    ]
    search_fields = [
        'numero_registro', 'nota_informativa_sicpip', 'departamento__nombre'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_registro', 'fecha_incautacion', 'hora_incautacion')
        }),
        ('Cantidad Incautada', {
            'fields': ('cantidad_unidades',)
        }),
        ('Lugar de Incautación', {
            'fields': ('departamento', 'provincia', 'distrito')
        }),
        ('Unidad Policial', {
            'fields': ('direccion_policial', 'direccion_especializada', 'division_policial', 
                      'departamento_policial', 'unidad_policial')
        }),
        ('Información Adicional', {
            'fields': ('nota_informativa_sicpip', 'tipo_intervencion')
        }),
        ('Metadatos del Sistema', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ['collapse']
        }),
    )


# KILOGRAMOS DE DROGAS

@admin.register(PlantillaKgPBC)
class PlantillaKgPBCAdmin(BaseDrogaAdmin):
    list_display = [
        'numero_registro', 'fecha_incautacion', 'cantidad_kilogramos', 
        'departamento', 'provincia', 'distrito', 'direccion_policial'
    ]
    list_filter = [
        'fecha_incautacion', 'departamento', 'direccion_policial', 'tipo_intervencion'
    ]
    search_fields = [
        'numero_registro', 'nota_informativa_sicpip', 'departamento__nombre'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_registro', 'fecha_incautacion', 'hora_incautacion')
        }),
        ('Cantidad Incautada', {
            'fields': ('cantidad_kilogramos',)
        }),
        ('Lugar de Incautación', {
            'fields': ('departamento', 'provincia', 'distrito')
        }),
        ('Unidad Policial', {
            'fields': ('direccion_policial', 'direccion_especializada', 'division_policial', 
                      'departamento_policial', 'unidad_policial')
        }),
        ('Información Adicional', {
            'fields': ('nota_informativa_sicpip', 'tipo_intervencion')
        }),
        ('Metadatos del Sistema', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ['collapse']
        }),
    )


@admin.register(PlantillaKgCC)
class PlantillaKgCCAdmin(BaseDrogaAdmin):
    list_display = [
        'numero_registro', 'fecha_incautacion', 'cantidad_kilogramos', 
        'departamento', 'provincia', 'distrito', 'direccion_policial'
    ]
    list_filter = [
        'fecha_incautacion', 'departamento', 'direccion_policial', 'tipo_intervencion'
    ]
    search_fields = [
        'numero_registro', 'nota_informativa_sicpip', 'departamento__nombre'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_registro', 'fecha_incautacion', 'hora_incautacion')
        }),
        ('Cantidad Incautada', {
            'fields': ('cantidad_kilogramos',)
        }),
        ('Lugar de Incautación', {
            'fields': ('departamento', 'provincia', 'distrito')
        }),
        ('Unidad Policial', {
            'fields': ('direccion_policial', 'direccion_especializada', 'division_policial', 
                      'departamento_policial', 'unidad_policial')
        }),
        ('Información Adicional', {
            'fields': ('nota_informativa_sicpip', 'tipo_intervencion')
        }),
        ('Metadatos del Sistema', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ['collapse']
        }),
    )


@admin.register(PlantillaKgMarihuana)
class PlantillaKgMarihuanaAdmin(BaseDrogaAdmin):
    list_display = [
        'numero_registro', 'fecha_incautacion', 'cantidad_kilogramos', 
        'departamento', 'provincia', 'distrito', 'direccion_policial'
    ]
    list_filter = [
        'fecha_incautacion', 'departamento', 'direccion_policial', 'tipo_intervencion'
    ]
    search_fields = [
        'numero_registro', 'nota_informativa_sicpip', 'departamento__nombre'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_registro', 'fecha_incautacion', 'hora_incautacion')
        }),
        ('Cantidad Incautada', {
            'fields': ('cantidad_kilogramos',)
        }),
        ('Lugar de Incautación', {
            'fields': ('departamento', 'provincia', 'distrito')
        }),
        ('Unidad Policial', {
            'fields': ('direccion_policial', 'direccion_especializada', 'division_policial', 
                      'departamento_policial', 'unidad_policial')
        }),
        ('Información Adicional', {
            'fields': ('nota_informativa_sicpip', 'tipo_intervencion')
        }),
        ('Metadatos del Sistema', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ['collapse']
        }),
    )


@admin.register(PlantillaKgLatexOpio)
class PlantillaKgLatexOpioAdmin(BaseDrogaAdmin):
    list_display = [
        'numero_registro', 'fecha_incautacion', 'cantidad_kilogramos', 
        'departamento', 'provincia', 'distrito', 'direccion_policial'
    ]
    list_filter = [
        'fecha_incautacion', 'departamento', 'direccion_policial', 'tipo_intervencion'
    ]
    search_fields = [
        'numero_registro', 'nota_informativa_sicpip', 'departamento__nombre'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_registro', 'fecha_incautacion', 'hora_incautacion')
        }),
        ('Cantidad Incautada', {
            'fields': ('cantidad_kilogramos',)
        }),
        ('Lugar de Incautación', {
            'fields': ('departamento', 'provincia', 'distrito')
        }),
        ('Unidad Policial', {
            'fields': ('direccion_policial', 'direccion_especializada', 'division_policial', 
                      'departamento_policial', 'unidad_policial')
        }),
        ('Información Adicional', {
            'fields': ('nota_informativa_sicpip', 'tipo_intervencion')
        }),
        ('Metadatos del Sistema', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ['collapse']
        }),
    )


@admin.register(PlantillaKgDrogaSintetica)
class PlantillaKgDrogaSinteticaAdmin(BaseDrogaAdmin):
    list_display = [
        'numero_registro', 'fecha_incautacion', 'cantidad_kilogramos', 
        'departamento', 'provincia', 'distrito', 'direccion_policial'
    ]
    list_filter = [
        'fecha_incautacion', 'departamento', 'direccion_policial', 'tipo_intervencion'
    ]
    search_fields = [
        'numero_registro', 'nota_informativa_sicpip', 'departamento__nombre'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_registro', 'fecha_incautacion', 'hora_incautacion')
        }),
        ('Cantidad Incautada', {
            'fields': ('cantidad_kilogramos',)
        }),
        ('Lugar de Incautación', {
            'fields': ('departamento', 'provincia', 'distrito')
        }),
        ('Unidad Policial', {
            'fields': ('direccion_policial', 'direccion_especializada', 'division_policial', 
                      'departamento_policial', 'unidad_policial')
        }),
        ('Información Adicional', {
            'fields': ('nota_informativa_sicpip', 'tipo_intervencion')
        }),
        ('Metadatos del Sistema', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ['collapse']
        }),
    )


@admin.register(PlantillaDetenidos)
class PlantillaDetenidosAdmin(BaseFormularioAdmin):
    list_display = [
        'numero_registro', 'fecha_detencion', 'apellido_paterno', 
        'apellido_materno', 'nombres', 'edad', 'genero', 
        'motivo_detencion', 'es_integrante_bbcc_oocc'
    ]
    list_filter = [
        'fecha_detencion', 'genero', 'motivo_detencion', 
        'es_integrante_bbcc_oocc', 'es_funcionario_publico',
        'departamento', 'nacionalidad', 'categoria_arma'
    ]
    search_fields = [
        'apellido_paterno', 'apellido_materno', 'nombres', 
        'numero_documento', 'nombre_bbcc_oocc', 'nombre_fiscal'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_registro', 'fecha_detencion', 'hora_detencion', 'motivo_detencion')
        }),
        ('Datos de la Persona', {
            'fields': ('apellido_paterno', 'apellido_materno', 'nombres', 'edad', 'genero',
                      'nacionalidad', 'tipo_documento', 'numero_documento')
        }),
        ('Ubicación de Detención', {
            'fields': ('departamento', 'provincia', 'distrito')
        }),
        ('Información Laboral', {
            'fields': ('es_funcionario_publico', 'entidad_publica', 'detalle_entidad')
        }),
        ('Organizaciones Criminales', {
            'fields': ('es_integrante_bbcc_oocc', 'nombre_bbcc_oocc')
        }),
        ('Información de Armas', {
            'fields': ('categoria_arma', 'tipo_arma')
        }),
        ('Delito Principal', {
            'fields': ('es_tentativa', 'delito_fuero', 'delito_general', 'delito_especifico', 'delito_subtipo')
        }),
        ('Delito Secundario (Opcional)', {
            'fields': ('es_tentativa_2', 'delito_fuero_2', 'delito_general_2', 'delito_especifico_2', 'delito_subtipo_2'),
            'classes': ['collapse']
        }),
        ('Primera Unidad Policial', {
            'fields': ('direccion_policial', 'direccion_especializada', 'division_policial', 
                      'departamento_policial', 'unidad_policial')
        }),
        ('Segunda Unidad Policial (Puesto a Disposición)', {
            'fields': ('direccion_policial_2', 'direccion_especializada_2', 'division_policial_2', 
                      'departamento_policial_2', 'unidad_policial_2'),
            'classes': ['collapse']
        }),
        ('Situación Procesal', {
            'fields': ('situacion_detenido', 'documento_libertad', 'documento_disposicion')
        }),
        ('Información Fiscal', {
            'fields': ('nombre_fiscal', 'fiscalia')
        }),
        ('Información Adicional', {
            'fields': ('nota_informativa_sicpip', 'tipo_intervencion', 'vehiculo_implicado')
        }),
        ('Metadatos del Sistema', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ['collapse']
        }),
    )


@admin.register(PlantillaMenoresRetenidos)
class PlantillaMenoresRetenidosAdmin(BaseFormularioAdmin):
    list_display = [
        'numero_registro', 'fecha_detencion', 'apellido_paterno', 
        'apellido_materno', 'nombres', 'edad', 'genero', 
        'motivo_detencion', 'es_integrante_bbcc_oocc'
    ]
    list_filter = [
        'fecha_detencion', 'genero', 'motivo_detencion', 
        'es_integrante_bbcc_oocc', 'departamento', 'nacionalidad'
    ]
    search_fields = [
        'apellido_paterno', 'apellido_materno', 'nombres', 
        'numero_documento', 'nombre_bbcc_oocc', 'nombre_fiscal'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_registro', 'fecha_detencion', 'hora_detencion', 'motivo_detencion')
        }),
        ('Datos del Menor', {
            'fields': ('apellido_paterno', 'apellido_materno', 'nombres', 'edad', 'genero',
                      'nacionalidad', 'tipo_documento', 'numero_documento')
        }),
        ('Ubicación de Detención', {
            'fields': ('departamento', 'provincia', 'distrito')
        }),
        ('Organizaciones Criminales', {
            'fields': ('es_integrante_bbcc_oocc', 'nombre_bbcc_oocc')
        }),
        ('Información de Armas', {
            'fields': ('categoria_arma', 'tipo_arma')
        }),
        ('Delito Principal', {
            'fields': ('es_tentativa', 'delito_fuero', 'delito_general', 'delito_especifico', 'delito_subtipo')
        }),
        ('Delito Secundario (Opcional)', {
            'fields': ('es_tentativa_2', 'delito_fuero_2', 'delito_general_2', 'delito_especifico_2', 'delito_subtipo_2'),
            'classes': ['collapse']
        }),
        ('Primera Unidad Policial', {
            'fields': ('direccion_policial', 'direccion_especializada', 'division_policial', 
                      'departamento_policial', 'unidad_policial')
        }),
        ('Segunda Unidad Policial (Puesto a Disposición)', {
            'fields': ('direccion_policial_2', 'direccion_especializada_2', 'division_policial_2', 
                      'departamento_policial_2', 'unidad_policial_2'),
            'classes': ['collapse']
        }),
        ('Situación Procesal', {
            'fields': ('situacion_detenido', 'documento_libertad', 'documento_disposicion')
        }),
        ('Información Fiscal', {
            'fields': ('nombre_fiscal', 'fiscalia')
        }),
        ('Información Adicional', {
            'fields': ('nota_informativa_sicpip',)
        }),
        ('Metadatos del Sistema', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ['collapse']
        }),
    )
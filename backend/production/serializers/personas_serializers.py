from rest_framework import serializers
from production.models import PlantillaRQ, PlantillaDetenidos, PlantillaMenoresRetenidos
from .base_serializers import (
    BaseFormularioSerializer, UbicacionMixin, UnidadPolicialMixin, 
    DelitoMixin, FormularioValidationMixin
)


# =============================================================================
# SERIALIZER PARA PLANTILLA RQ
# =============================================================================

class PlantillaRQSerializer(
    BaseFormularioSerializer, 
    UbicacionMixin, 
    UnidadPolicialMixin, 
    DelitoMixin,
    FormularioValidationMixin
):
    """
    Serializer para el formulario de Requisitorias (RQ)
    """
    
    # Campos anidados para lectura
    ubicacion_completa = serializers.SerializerMethodField()
    unidad_policial_completa = serializers.SerializerMethodField()
    delito_principal_completo = serializers.SerializerMethodField()
    delito_secundario_completo = serializers.SerializerMethodField()
    
    # Datos de referencia anidados
    nacionalidad_data = serializers.SerializerMethodField()
    tipo_documento_data = serializers.SerializerMethodField()
    tipo_requisitoria_data = serializers.SerializerMethodField()
    
    class Meta:
        model = PlantillaRQ
        fields = BaseFormularioSerializer.Meta.fields + [
            # Campos específicos de fecha
            'fecha_detencion', 'hora_detencion',
            
            # Datos de la persona
            'apellido_paterno', 'apellido_materno', 'nombres', 'edad', 'genero',
            'nacionalidad', 'nacionalidad_data', 'tipo_documento', 'tipo_documento_data', 
            'numero_documento',
            
            # Ubicación
            'departamento', 'provincia', 'distrito', 'ubicacion_completa',
            
            # Información de requisitoria
            'tipo_requisitoria', 'tipo_requisitoria_data', 'esta_en_lista_mas_buscados',
            
            # Información laboral
            'es_funcionario_publico', 'entidad_publica', 'detalle_entidad',
            
            # Delito principal
            'es_tentativa', 'delito_fuero', 'delito_general', 'delito_especifico', 'delito_subtipo',
            'delito_principal_completo',
            
            # Delito secundario
            'es_tentativa_2', 'delito_fuero_2', 'delito_general_2', 'delito_especifico_2', 
            'delito_subtipo_2', 'delito_secundario_completo',
            
            # Unidad policial
            'direccion_policial', 'direccion_especializada', 'division_policial',
            'departamento_policial', 'unidad_policial', 'unidad_policial_completa',
            
            # Información judicial
            'autoridad_que_solicita', 'documento_que_solicita',
            
            # Información adicional
            'nota_informativa_sicpip', 'tipo_intervencion'
        ]
        read_only_fields = BaseFormularioSerializer.Meta.fields
    
    def get_ubicacion_completa(self, obj):
        return self.get_ubicacion_data(obj)
    
    def get_unidad_policial_completa(self, obj):
        return self.get_unidad_policial_data(obj)
    
    def get_delito_principal_completo(self, obj):
        return self.get_delito_principal_data(obj)
    
    def get_delito_secundario_completo(self, obj):
        return self.get_delito_secundario_data(obj)
    
    def get_nacionalidad_data(self, obj):
        if obj.nacionalidad:
            return {
                'id': obj.nacionalidad.id,
                'nombre': obj.nacionalidad.nombre,
                'codigo': obj.nacionalidad.codigo
            }
        return None
    
    def get_tipo_documento_data(self, obj):
        if obj.tipo_documento:
            return {
                'id': obj.tipo_documento.id,
                'nombre': obj.tipo_documento.nombre,
                'codigo': obj.tipo_documento.codigo
            }
        return None
    
    def get_tipo_requisitoria_data(self, obj):
        if obj.tipo_requisitoria:
            return {
                'id': obj.tipo_requisitoria.id,
                'nombre': obj.tipo_requisitoria.nombre,
                'descripcion': obj.tipo_requisitoria.descripcion
            }
        return None
    
    def validate(self, attrs):
        """Validaciones personalizadas"""
        attrs = self.validate_delito_consistency(attrs)
        attrs = self.validate_ubicacion_consistency(attrs)
        
        # Validación específica para funcionario público
        if attrs.get('es_funcionario_publico') != 'PARTICULARES':
            if not attrs.get('entidad_publica'):
                raise serializers.ValidationError({
                    'entidad_publica': 'Este campo es obligatorio si no es PARTICULAR.'
                })
        
        return attrs


# =============================================================================
# SERIALIZER PARA PLANTILLA DETENIDOS
# =============================================================================

class PlantillaDetenidosSerializer(
    BaseFormularioSerializer, 
    UbicacionMixin, 
    UnidadPolicialMixin, 
    DelitoMixin,
    FormularioValidationMixin
):
    """
    Serializer para el formulario de Detenidos por Diversos Delitos
    """
    
    # Campos anidados para lectura
    ubicacion_completa = serializers.SerializerMethodField()
    unidad_policial_completa = serializers.SerializerMethodField()
    unidad_policial_2_completa = serializers.SerializerMethodField()
    delito_principal_completo = serializers.SerializerMethodField()
    delito_secundario_completo = serializers.SerializerMethodField()
    
    # Datos de referencia anidados
    nacionalidad_data = serializers.SerializerMethodField()
    tipo_documento_data = serializers.SerializerMethodField()
    categoria_arma_data = serializers.SerializerMethodField()
    tipo_arma_data = serializers.SerializerMethodField()
    situacion_detenido_data = serializers.SerializerMethodField()
    fiscalia_data = serializers.SerializerMethodField()
    
    class Meta:
        model = PlantillaDetenidos
        fields = BaseFormularioSerializer.Meta.fields + [
            # Campos específicos de fecha
            'fecha_detencion', 'hora_detencion', 'motivo_detencion',
            
            # Datos de la persona
            'apellido_paterno', 'apellido_materno', 'nombres', 'edad', 'genero',
            'nacionalidad', 'nacionalidad_data', 'tipo_documento', 'tipo_documento_data', 
            'numero_documento',
            
            # Ubicación
            'departamento', 'provincia', 'distrito', 'ubicacion_completa',
            
            # Información laboral
            'es_funcionario_publico', 'entidad_publica', 'detalle_entidad',
            
            # Organizaciones criminales
            'es_integrante_bbcc_oocc', 'nombre_bbcc_oocc',
            
            # Información de armas
            'categoria_arma', 'categoria_arma_data', 'tipo_arma', 'tipo_arma_data',
            
            # Delito principal
            'es_tentativa', 'delito_fuero', 'delito_general', 'delito_especifico', 'delito_subtipo',
            'delito_principal_completo',
            
            # Delito secundario
            'es_tentativa_2', 'delito_fuero_2', 'delito_general_2', 'delito_especifico_2', 
            'delito_subtipo_2', 'delito_secundario_completo',
            
            # Primera unidad policial
            'direccion_policial', 'direccion_especializada', 'division_policial',
            'departamento_policial', 'unidad_policial', 'unidad_policial_completa',
            
            # Segunda unidad policial (Puesto a Disposición)
            'direccion_policial_2', 'direccion_especializada_2', 'division_policial_2',
            'departamento_policial_2', 'unidad_policial_2', 'unidad_policial_2_completa',
            
            # Situación procesal
            'situacion_detenido', 'situacion_detenido_data', 'documento_libertad', 'documento_disposicion',
            
            # Información fiscal
            'nombre_fiscal', 'fiscalia', 'fiscalia_data',
            
            # Información adicional
            'nota_informativa_sicpip', 'tipo_intervencion', 'vehiculo_implicado'
        ]
        read_only_fields = BaseFormularioSerializer.Meta.fields
    
    def get_ubicacion_completa(self, obj):
        return self.get_ubicacion_data(obj)
    
    def get_unidad_policial_completa(self, obj):
        return self.get_unidad_policial_data(obj)
    
    def get_unidad_policial_2_completa(self, obj):
        """Datos de la segunda unidad policial"""
        data = {}
        
        if obj.direccion_policial_2:
            data['direccion_policial_2'] = {
                'id': obj.direccion_policial_2.id,
                'nombre': obj.direccion_policial_2.nombre,
                'sigla': obj.direccion_policial_2.sigla
            }
        
        if obj.direccion_especializada_2:
            data['direccion_especializada_2'] = {
                'id': obj.direccion_especializada_2.id,
                'nombre': obj.direccion_especializada_2.nombre,
                'sigla': obj.direccion_especializada_2.sigla
            }
        
        if obj.division_policial_2:
            data['division_policial_2'] = {
                'id': obj.division_policial_2.id,
                'nombre': obj.division_policial_2.nombre,
                'sigla': obj.division_policial_2.sigla
            }
        
        if obj.departamento_policial_2:
            data['departamento_policial_2'] = {
                'id': obj.departamento_policial_2.id,
                'nombre': obj.departamento_policial_2.nombre,
                'sigla': obj.departamento_policial_2.sigla
            }
        
        if obj.unidad_policial_2:
            data['unidad_policial_2'] = {
                'id': obj.unidad_policial_2.id,
                'nombre': obj.unidad_policial_2.nombre,
                'sigla': obj.unidad_policial_2.sigla
            }
        
        return data
    
    def get_delito_principal_completo(self, obj):
        return self.get_delito_principal_data(obj)
    
    def get_delito_secundario_completo(self, obj):
        return self.get_delito_secundario_data(obj)
    
    def get_nacionalidad_data(self, obj):
        if obj.nacionalidad:
            return {
                'id': obj.nacionalidad.id,
                'nombre': obj.nacionalidad.nombre,
                'codigo': obj.nacionalidad.codigo
            }
        return None
    
    def get_tipo_documento_data(self, obj):
        if obj.tipo_documento:
            return {
                'id': obj.tipo_documento.id,
                'nombre': obj.tipo_documento.nombre,
                'codigo': obj.tipo_documento.codigo
            }
        return None
    
    def get_categoria_arma_data(self, obj):
        if obj.categoria_arma:
            return {
                'id': obj.categoria_arma.id,
                'nombre': obj.categoria_arma.nombre,
                'descripcion': obj.categoria_arma.descripcion
            }
        return None
    
    def get_tipo_arma_data(self, obj):
        if obj.tipo_arma:
            return {
                'id': obj.tipo_arma.id,
                'nombre': obj.tipo_arma.nombre,
                'descripcion': obj.tipo_arma.descripcion
            }
        return None
    
    def get_situacion_detenido_data(self, obj):
        if obj.situacion_detenido:
            return {
                'id': obj.situacion_detenido.id,
                'nombre': obj.situacion_detenido.nombre,
                'descripcion': obj.situacion_detenido.descripcion
            }
        return None
    
    def get_fiscalia_data(self, obj):
        if obj.fiscalia:
            return {
                'id': obj.fiscalia.id,
                'nombre': obj.fiscalia.nombre,
                'direccion': obj.fiscalia.direccion,
                'telefono': obj.fiscalia.telefono
            }
        return None
    
    def validate(self, attrs):
        """Validaciones personalizadas"""
        attrs = self.validate_delito_consistency(attrs)
        attrs = self.validate_ubicacion_consistency(attrs)
        
        # Validación específica para funcionario público
        if attrs.get('es_funcionario_publico') != 'PARTICULARES':
            if not attrs.get('entidad_publica'):
                raise serializers.ValidationError({
                    'entidad_publica': 'Este campo es obligatorio si no es PARTICULAR.'
                })
        
        # Validación para BBCC/OOCC
        if attrs.get('es_integrante_bbcc_oocc') == 'SÍ':
            if not attrs.get('nombre_bbcc_oocc'):
                raise serializers.ValidationError({
                    'nombre_bbcc_oocc': 'Este campo es obligatorio si es integrante de BBCC/OOCC.'
                })
        
        return attrs


# =============================================================================
# SERIALIZER PARA PLANTILLA MENORES RETENIDOS
# =============================================================================

class PlantillaMenoresRetenidosSerializer(
    BaseFormularioSerializer, 
    UbicacionMixin, 
    UnidadPolicialMixin, 
    DelitoMixin,
    FormularioValidationMixin
):
    """
    Serializer para el formulario de Menores Retenidos por Diversos Delitos
    """
    
    # Campos anidados para lectura (similar a Detenidos pero sin funcionario público)
    ubicacion_completa = serializers.SerializerMethodField()
    unidad_policial_completa = serializers.SerializerMethodField()
    unidad_policial_2_completa = serializers.SerializerMethodField()
    delito_principal_completo = serializers.SerializerMethodField()
    delito_secundario_completo = serializers.SerializerMethodField()
    
    # Datos de referencia anidados
    nacionalidad_data = serializers.SerializerMethodField()
    tipo_documento_data = serializers.SerializerMethodField()
    categoria_arma_data = serializers.SerializerMethodField()
    tipo_arma_data = serializers.SerializerMethodField()
    situacion_detenido_data = serializers.SerializerMethodField()
    fiscalia_data = serializers.SerializerMethodField()
    
    class Meta:
        model = PlantillaMenoresRetenidos
        fields = BaseFormularioSerializer.Meta.fields + [
            # Campos específicos de fecha
            'fecha_detencion', 'hora_detencion', 'motivo_detencion',
            
            # Datos del menor
            'apellido_paterno', 'apellido_materno', 'nombres', 'edad', 'genero',
            'nacionalidad', 'nacionalidad_data', 'tipo_documento', 'tipo_documento_data', 
            'numero_documento',
            
            # Ubicación
            'departamento', 'provincia', 'distrito', 'ubicacion_completa',
            
            # Organizaciones criminales
            'es_integrante_bbcc_oocc', 'nombre_bbcc_oocc',
            
            # Información de armas
            'categoria_arma', 'categoria_arma_data', 'tipo_arma', 'tipo_arma_data',
            
            # Delito principal
            'es_tentativa', 'delito_fuero', 'delito_general', 'delito_especifico', 'delito_subtipo',
            'delito_principal_completo',
            
            # Delito secundario
            'es_tentativa_2', 'delito_fuero_2', 'delito_general_2', 'delito_especifico_2', 
            'delito_subtipo_2', 'delito_secundario_completo',
            
            # Primera unidad policial
            'direccion_policial', 'direccion_especializada', 'division_policial',
            'departamento_policial', 'unidad_policial', 'unidad_policial_completa',
            
            # Segunda unidad policial (Puesto a Disposición)
            'direccion_policial_2', 'direccion_especializada_2', 'division_policial_2',
            'departamento_policial_2', 'unidad_policial_2', 'unidad_policial_2_completa',
            
            # Situación procesal
            'situacion_detenido', 'situacion_detenido_data', 'documento_libertad', 'documento_disposicion',
            
            # Información fiscal
            'nombre_fiscal', 'fiscalia', 'fiscalia_data',
            
            # Información adicional
            'nota_informativa_sicpip'
        ]
        read_only_fields = BaseFormularioSerializer.Meta.fields
    
    # Métodos similares a PlantillaDetenidosSerializer
    def get_ubicacion_completa(self, obj):
        return self.get_ubicacion_data(obj)
    
    def get_unidad_policial_completa(self, obj):
        return self.get_unidad_policial_data(obj)
    
    def get_unidad_policial_2_completa(self, obj):
        """Datos de la segunda unidad policial"""
        data = {}
        
        if obj.direccion_policial_2:
            data['direccion_policial_2'] = {
                'id': obj.direccion_policial_2.id,
                'nombre': obj.direccion_policial_2.nombre,
                'sigla': obj.direccion_policial_2.sigla
            }
        
        if obj.direccion_especializada_2:
            data['direccion_especializada_2'] = {
                'id': obj.direccion_especializada_2.id,
                'nombre': obj.direccion_especializada_2.nombre,
                'sigla': obj.direccion_especializada_2.sigla
            }
        
        return data
    
    def get_delito_principal_completo(self, obj):
        return self.get_delito_principal_data(obj)
    
    def get_delito_secundario_completo(self, obj):
        return self.get_delito_secundario_data(obj)
    
    def get_nacionalidad_data(self, obj):
        if obj.nacionalidad:
            return {
                'id': obj.nacionalidad.id,
                'nombre': obj.nacionalidad.nombre,
                'codigo': obj.nacionalidad.codigo
            }
        return None
    
    def get_tipo_documento_data(self, obj):
        if obj.tipo_documento:
            return {
                'id': obj.tipo_documento.id,
                'nombre': obj.tipo_documento.nombre,
                'codigo': obj.tipo_documento.codigo
            }
        return None
    
    def get_categoria_arma_data(self, obj):
        if obj.categoria_arma:
            return {
                'id': obj.categoria_arma.id,
                'nombre': obj.categoria_arma.nombre,
                'descripcion': obj.categoria_arma.descripcion
            }
        return None
    
    def get_tipo_arma_data(self, obj):
        if obj.tipo_arma:
            return {
                'id': obj.tipo_arma.id,
                'nombre': obj.tipo_arma.nombre,
                'descripcion': obj.tipo_arma.descripcion
            }
        return None
    
    def get_situacion_detenido_data(self, obj):
        if obj.situacion_detenido:
            return {
                'id': obj.situacion_detenido.id,
                'nombre': obj.situacion_detenido.nombre,
                'descripcion': obj.situacion_detenido.descripcion
            }
        return None
    
    def get_fiscalia_data(self, obj):
        if obj.fiscalia:
            return {
                'id': obj.fiscalia.id,
                'nombre': obj.fiscalia.nombre,
                'direccion': obj.fiscalia.direccion,
                'telefono': obj.fiscalia.telefono
            }
        return None
    
    def validate(self, attrs):
        """Validaciones personalizadas"""
        attrs = self.validate_delito_consistency(attrs)
        attrs = self.validate_ubicacion_consistency(attrs)
        
        # Validación específica para menores (edad máxima)
        if attrs.get('edad') and attrs['edad'] >= 18:
            raise serializers.ValidationError({
                'edad': 'Para menores retenidos, la edad debe ser menor a 18 años.'
            })
        
        # Validación para BBCC/OOCC
        if attrs.get('es_integrante_bbcc_oocc') == 'SÍ':
            if not attrs.get('nombre_bbcc_oocc'):
                raise serializers.ValidationError({
                    'nombre_bbcc_oocc': 'Este campo es obligatorio si es integrante de BBCC/OOCC.'
                })
        
        return attrs
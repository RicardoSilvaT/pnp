from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


# =============================================================================
# SERIALIZERS BASE Y MIXINS REUTILIZABLES
# =============================================================================

class BaseFormularioSerializer(serializers.ModelSerializer):
    """
    Serializer base para todos los formularios con campos comunes
    """
    # Campos de solo lectura para metadatos
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    
    # Número de registro auto-generado
    numero_registro = serializers.IntegerField(read_only=True)
    
    class Meta:
        abstract = True
        fields = [
            'id', 'numero_registro', 'created_at', 'updated_at', 
            'created_by', 'updated_by'
        ]


class UbicacionMixin:
    """
    Mixin para serializers que incluyen ubicación geográfica
    """
    def get_ubicacion_data(self, obj):
        """Método helper para obtener datos de ubicación completos"""
        if hasattr(obj, 'distrito'):
            return {
                'departamento': {
                    'id': obj.departamento.id,
                    'nombre': obj.departamento.nombre,
                    'codigo': obj.departamento.codigo
                },
                'provincia': {
                    'id': obj.provincia.id,
                    'nombre': obj.provincia.nombre,
                    'codigo': obj.provincia.codigo
                },
                'distrito': {
                    'id': obj.distrito.id,
                    'nombre': obj.distrito.nombre,
                    'codigo': obj.distrito.codigo
                }
            }
        return None


class UnidadPolicialMixin:
    """
    Mixin para serializers que incluyen datos de unidad policial
    """
    def get_unidad_policial_data(self, obj):
        """Método helper para obtener datos de unidad policial completos"""
        data = {}
        
        if hasattr(obj, 'direccion_policial') and obj.direccion_policial:
            data['direccion_policial'] = {
                'id': obj.direccion_policial.id,
                'nombre': obj.direccion_policial.nombre,
                'sigla': obj.direccion_policial.sigla
            }
        
        if hasattr(obj, 'direccion_especializada') and obj.direccion_especializada:
            data['direccion_especializada'] = {
                'id': obj.direccion_especializada.id,
                'nombre': obj.direccion_especializada.nombre,
                'sigla': obj.direccion_especializada.sigla
            }
        
        if hasattr(obj, 'division_policial') and obj.division_policial:
            data['division_policial'] = {
                'id': obj.division_policial.id,
                'nombre': obj.division_policial.nombre,
                'sigla': obj.division_policial.sigla
            }
        
        if hasattr(obj, 'departamento_policial') and obj.departamento_policial:
            data['departamento_policial'] = {
                'id': obj.departamento_policial.id,
                'nombre': obj.departamento_policial.nombre,
                'sigla': obj.departamento_policial.sigla
            }
        
        if hasattr(obj, 'unidad_policial') and obj.unidad_policial:
            data['unidad_policial'] = {
                'id': obj.unidad_policial.id,
                'nombre': obj.unidad_policial.nombre,
                'sigla': obj.unidad_policial.sigla
            }
        
        return data


class DelitoMixin:
    """
    Mixin para serializers que incluyen información de delitos
    """
    def get_delito_principal_data(self, obj):
        """Método helper para obtener datos del delito principal"""
        if hasattr(obj, 'delito_subtipo') and obj.delito_subtipo:
            return {
                'es_tentativa': obj.es_tentativa,
                'fuero': {
                    'id': obj.delito_fuero.id,
                    'nombre': obj.delito_fuero.nombre
                },
                'general': {
                    'id': obj.delito_general.id,
                    'nombre': obj.delito_general.nombre
                },
                'especifico': {
                    'id': obj.delito_especifico.id,
                    'nombre': obj.delito_especifico.nombre
                },
                'subtipo': {
                    'id': obj.delito_subtipo.id,
                    'nombre': obj.delito_subtipo.nombre
                }
            }
        return None
    
    def get_delito_secundario_data(self, obj):
        """Método helper para obtener datos del delito secundario"""
        if hasattr(obj, 'delito_subtipo_2') and obj.delito_subtipo_2:
            return {
                'es_tentativa_2': obj.es_tentativa_2,
                'fuero': {
                    'id': obj.delito_fuero_2.id,
                    'nombre': obj.delito_fuero_2.nombre
                },
                'general': {
                    'id': obj.delito_general_2.id,
                    'nombre': obj.delito_general_2.nombre
                },
                'especifico': {
                    'id': obj.delito_especifico_2.id,
                    'nombre': obj.delito_especifico_2.nombre
                },
                'subtipo': {
                    'id': obj.delito_subtipo_2.id,
                    'nombre': obj.delito_subtipo_2.nombre
                }
            }
        return None


# =============================================================================
# SERIALIZERS PARA RESPUESTAS ANIDADAS
# =============================================================================

class SimpleReferenceSerializer(serializers.ModelSerializer):
    """
    Serializer simple para referencias anidadas (solo id y nombre)
    """
    class Meta:
        fields = ['id', 'nombre']


class SimpleReferenceWithCodeSerializer(serializers.ModelSerializer):
    """
    Serializer simple para referencias con código
    """
    class Meta:
        fields = ['id', 'nombre', 'codigo']


class SimpleReferenceWithSiglaSerializer(serializers.ModelSerializer):
    """
    Serializer simple para referencias con sigla
    """
    class Meta:
        fields = ['id', 'nombre', 'sigla']


# =============================================================================
# SERIALIZERS PARA FILTROS CASCADA
# =============================================================================

class ProvinciaFiltradaSerializer(serializers.ModelSerializer):
    """
    Serializer para provincias filtradas por departamento
    """
    class Meta:
        fields = ['id', 'nombre', 'codigo', 'departamento']


class DistritoFiltradoSerializer(serializers.ModelSerializer):
    """
    Serializer para distritos filtrados por provincia
    """
    class Meta:
        fields = ['id', 'nombre', 'codigo', 'provincia']


class DelitoGeneralFiltradoSerializer(serializers.ModelSerializer):
    """
    Serializer para delitos generales filtrados por fuero
    """
    class Meta:
        fields = ['id', 'nombre', 'descripcion', 'delito_fuero']


class DelitoEspecificoFiltradoSerializer(serializers.ModelSerializer):
    """
    Serializer para delitos específicos filtrados por general
    """
    class Meta:
        fields = ['id', 'nombre', 'descripcion', 'delito_general']


class DelitoSubtipoFiltradoSerializer(serializers.ModelSerializer):
    """
    Serializer para delitos subtipos filtrados por específico
    """
    class Meta:
        fields = ['id', 'nombre', 'descripcion', 'delito_especifico']


class DireccionEspecializadaFiltradaSerializer(serializers.ModelSerializer):
    """
    Serializer para direcciones especializadas filtradas por dirección policial
    """
    class Meta:
        fields = ['id', 'nombre', 'sigla', 'direccion_policial']


class TipoArmaFiltradoSerializer(serializers.ModelSerializer):
    """
    Serializer para tipos de arma filtrados por categoría
    """
    class Meta:
        fields = ['id', 'nombre', 'descripcion', 'categoria_arma']


# =============================================================================
# UTILIDADES PARA VALIDACIÓN
# =============================================================================

class FormularioValidationMixin:
    """
    Mixin para validaciones comunes en formularios
    """
    
    def validate_edad(self, value):
        """Validar que la edad esté en rango válido"""
        if value < 0 or value > 120:
            raise serializers.ValidationError(
                "La edad debe estar entre 0 y 120 años."
            )
        return value
    
    def validate_numero_documento(self, value):
        """Validar formato básico de número de documento"""
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                "El número de documento debe tener al menos 3 caracteres."
            )
        return value.strip()
    
    def validate_cantidad_unidades(self, value):
        """Validar que la cantidad de unidades sea positiva"""
        if value <= 0:
            raise serializers.ValidationError(
                "La cantidad de unidades debe ser mayor a 0."
            )
        return value
    
    def validate_cantidad_kilogramos(self, value):
        """Validar que el peso sea positivo"""
        if value <= 0:
            raise serializers.ValidationError(
                "La cantidad de kilogramos debe ser mayor a 0."
            )
        return value
    
    def validate_delito_consistency(self, attrs):
        """Validar consistencia en la jerarquía de delitos"""
        # Validar delito principal
        if all(k in attrs for k in ['delito_fuero', 'delito_general', 'delito_especifico', 'delito_subtipo']):
            if attrs['delito_general'].delito_fuero != attrs['delito_fuero']:
                raise serializers.ValidationError(
                    "El delito general no corresponde al fuero seleccionado."
                )
            if attrs['delito_especifico'].delito_general != attrs['delito_general']:
                raise serializers.ValidationError(
                    "El delito específico no corresponde al delito general seleccionado."
                )
            if attrs['delito_subtipo'].delito_especifico != attrs['delito_especifico']:
                raise serializers.ValidationError(
                    "El subtipo de delito no corresponde al delito específico seleccionado."
                )
        
        # Validar delito secundario si existe
        if attrs.get('es_tentativa_2') == 'SÍ':
            required_fields = ['delito_fuero_2', 'delito_general_2', 'delito_especifico_2', 'delito_subtipo_2']
            if not all(attrs.get(field) for field in required_fields):
                raise serializers.ValidationError(
                    "Si hay delito secundario, todos los campos del delito secundario son obligatorios."
                )
        
        return attrs
    
    def validate_ubicacion_consistency(self, attrs):
        """Validar consistencia en la jerarquía de ubicación"""
        if all(k in attrs for k in ['departamento', 'provincia', 'distrito']):
            if attrs['provincia'].departamento != attrs['departamento']:
                raise serializers.ValidationError(
                    "La provincia no corresponde al departamento seleccionado."
                )
            if attrs['distrito'].provincia != attrs['provincia']:
                raise serializers.ValidationError(
                    "El distrito no corresponde a la provincia seleccionada."
                )
        return attrs
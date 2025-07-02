from rest_framework import serializers
from production.models import (
    PlantillaEnvPBC, PlantillaEnvCC, PlantillaEnvMarihuana,
    PlantillaKgPBC, PlantillaKgCC, PlantillaKgMarihuana,
    PlantillaKgLatexOpio, PlantillaKgDrogaSintetica
)
from .base_serializers import (
    BaseFormularioSerializer, UbicacionMixin, UnidadPolicialMixin, 
    FormularioValidationMixin
)


# =============================================================================
# SERIALIZER BASE PARA FORMULARIOS DE DROGAS
# =============================================================================

class BaseDrogaSerializer(
    BaseFormularioSerializer, 
    UbicacionMixin, 
    UnidadPolicialMixin,
    FormularioValidationMixin
):
    """
    Serializer base para todos los formularios de drogas
    """
    
    # Campos anidados para lectura
    ubicacion_completa = serializers.SerializerMethodField()
    unidad_policial_completa = serializers.SerializerMethodField()
    
    def get_ubicacion_completa(self, obj):
        return self.get_ubicacion_data(obj)
    
    def get_unidad_policial_completa(self, obj):
        return self.get_unidad_policial_data(obj)
    
    def validate(self, attrs):
        """Validaciones comunes para formularios de drogas"""
        attrs = self.validate_ubicacion_consistency(attrs)
        return attrs
    
    class Meta:
        abstract = True
        fields = BaseFormularioSerializer.Meta.fields + [
            # Campos específicos de fecha para drogas
            'fecha_incautacion', 'hora_incautacion',
            
            # Ubicación de incautación
            'departamento', 'provincia', 'distrito', 'ubicacion_completa',
            
            # Unidad policial
            'direccion_policial', 'direccion_especializada', 'division_policial',
            'departamento_policial', 'unidad_policial', 'unidad_policial_completa',
            
            # Información adicional
            'nota_informativa_sicpip', 'tipo_intervencion'
        ]


# =============================================================================
# SERIALIZERS PARA ENVOLTORIOS DE DROGAS
# =============================================================================

class PlantillaEnvPBCSerializer(BaseDrogaSerializer):
    """
    Serializer para el formulario de Envoltorios de Pasta Básica de Cocaína
    """
    
    class Meta:
        model = PlantillaEnvPBC
        fields = BaseDrogaSerializer.Meta.fields + [
            'cantidad_unidades'
        ]
        read_only_fields = BaseFormularioSerializer.Meta.fields
    
    def validate(self, attrs):
        """Validaciones específicas para ENV PBC"""
        attrs = super().validate(attrs)
        
        # Validar cantidad de unidades
        if 'cantidad_unidades' in attrs:
            attrs = {'cantidad_unidades': self.validate_cantidad_unidades(attrs['cantidad_unidades']), **attrs}
        
        return attrs


class PlantillaEnvCCSerializer(BaseDrogaSerializer):
    """
    Serializer para el formulario de Envoltorios de Clorhidrato de Cocaína
    """
    
    class Meta:
        model = PlantillaEnvCC
        fields = BaseDrogaSerializer.Meta.fields + [
            'cantidad_unidades'
        ]
        read_only_fields = BaseFormularioSerializer.Meta.fields
    
    def validate(self, attrs):
        """Validaciones específicas para ENV CC"""
        attrs = super().validate(attrs)
        
        # Validar cantidad de unidades
        if 'cantidad_unidades' in attrs:
            attrs = {'cantidad_unidades': self.validate_cantidad_unidades(attrs['cantidad_unidades']), **attrs}
        
        return attrs


class PlantillaEnvMarihuanaSerializer(BaseDrogaSerializer):
    """
    Serializer para el formulario de Envoltorios de Marihuana
    """
    
    class Meta:
        model = PlantillaEnvMarihuana
        fields = BaseDrogaSerializer.Meta.fields + [
            'cantidad_unidades'
        ]
        read_only_fields = BaseFormularioSerializer.Meta.fields
    
    def validate(self, attrs):
        """Validaciones específicas para ENV MARIHUANA"""
        attrs = super().validate(attrs)
        
        # Validar cantidad de unidades
        if 'cantidad_unidades' in attrs:
            attrs = {'cantidad_unidades': self.validate_cantidad_unidades(attrs['cantidad_unidades']), **attrs}
        
        return attrs


# =============================================================================
# SERIALIZERS PARA KILOGRAMOS DE DROGAS
# =============================================================================

class PlantillaKgPBCSerializer(BaseDrogaSerializer):
    """
    Serializer para el formulario de Kilogramos de Pasta Básica de Cocaína
    """
    
    class Meta:
        model = PlantillaKgPBC
        fields = BaseDrogaSerializer.Meta.fields + [
            'cantidad_kilogramos'
        ]
        read_only_fields = BaseFormularioSerializer.Meta.fields
    
    def validate(self, attrs):
        """Validaciones específicas para KG PBC"""
        attrs = super().validate(attrs)
        
        # Validar cantidad de kilogramos
        if 'cantidad_kilogramos' in attrs:
            attrs = {'cantidad_kilogramos': self.validate_cantidad_kilogramos(attrs['cantidad_kilogramos']), **attrs}
        
        return attrs


class PlantillaKgCCSerializer(BaseDrogaSerializer):
    """
    Serializer para el formulario de Kilogramos de Clorhidrato de Cocaína
    """
    
    class Meta:
        model = PlantillaKgCC
        fields = BaseDrogaSerializer.Meta.fields + [
            'cantidad_kilogramos'
        ]
        read_only_fields = BaseFormularioSerializer.Meta.fields
    
    def validate(self, attrs):
        """Validaciones específicas para KG CC"""
        attrs = super().validate(attrs)
        
        # Validar cantidad de kilogramos
        if 'cantidad_kilogramos' in attrs:
            attrs = {'cantidad_kilogramos': self.validate_cantidad_kilogramos(attrs['cantidad_kilogramos']), **attrs}
        
        return attrs


class PlantillaKgMarihuanaSerializer(BaseDrogaSerializer):
    """
    Serializer para el formulario de Kilogramos de Marihuana
    """
    
    class Meta:
        model = PlantillaKgMarihuana
        fields = BaseDrogaSerializer.Meta.fields + [
            'cantidad_kilogramos'
        ]
        read_only_fields = BaseFormularioSerializer.Meta.fields
    
    def validate(self, attrs):
        """Validaciones específicas para KG MARIHUANA"""
        attrs = super().validate(attrs)
        
        # Validar cantidad de kilogramos
        if 'cantidad_kilogramos' in attrs:
            attrs = {'cantidad_kilogramos': self.validate_cantidad_kilogramos(attrs['cantidad_kilogramos']), **attrs}
        
        return attrs


class PlantillaKgLatexOpioSerializer(BaseDrogaSerializer):
    """
    Serializer para el formulario de Kilogramos de Látex de Opio
    """
    
    class Meta:
        model = PlantillaKgLatexOpio
        fields = BaseDrogaSerializer.Meta.fields + [
            'cantidad_kilogramos'
        ]
        read_only_fields = BaseFormularioSerializer.Meta.fields
    
    def validate(self, attrs):
        """Validaciones específicas para KG LÁTEX OPIO"""
        attrs = super().validate(attrs)
        
        # Validar cantidad de kilogramos
        if 'cantidad_kilogramos' in attrs:
            attrs = {'cantidad_kilogramos': self.validate_cantidad_kilogramos(attrs['cantidad_kilogramos']), **attrs}
        
        return attrs


class PlantillaKgDrogaSinteticaSerializer(BaseDrogaSerializer):
    """
    Serializer para el formulario de Kilogramos de Droga Sintética
    """
    
    class Meta:
        model = PlantillaKgDrogaSintetica
        fields = BaseDrogaSerializer.Meta.fields + [
            'cantidad_kilogramos'
        ]
        read_only_fields = BaseFormularioSerializer.Meta.fields
    
    def validate(self, attrs):
        """Validaciones específicas para KG DROGA SINTÉTICA"""
        attrs = super().validate(attrs)
        
        # Validar cantidad de kilogramos
        if 'cantidad_kilogramos' in attrs:
            attrs = {'cantidad_kilogramos': self.validate_cantidad_kilogramos(attrs['cantidad_kilogramos']), **attrs}
        
        return attrs


# =============================================================================
# SERIALIZERS SIMPLIFICADOS PARA LISTADOS
# =============================================================================

class PlantillaEnvPBCListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listados de ENV PBC
    """
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    direccion_policial_sigla = serializers.CharField(source='direccion_policial.sigla', read_only=True)
    
    class Meta:
        model = PlantillaEnvPBC
        fields = [
            'id', 'numero_registro', 'fecha_incautacion', 'cantidad_unidades',
            'departamento_nombre', 'direccion_policial_sigla', 'tipo_intervencion'
        ]


class PlantillaEnvCCListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listados de ENV CC
    """
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    direccion_policial_sigla = serializers.CharField(source='direccion_policial.sigla', read_only=True)
    
    class Meta:
        model = PlantillaEnvCC
        fields = [
            'id', 'numero_registro', 'fecha_incautacion', 'cantidad_unidades',
            'departamento_nombre', 'direccion_policial_sigla', 'tipo_intervencion'
        ]


class PlantillaEnvMarihuanaListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listados de ENV MARIHUANA
    """
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    direccion_policial_sigla = serializers.CharField(source='direccion_policial.sigla', read_only=True)
    
    class Meta:
        model = PlantillaEnvMarihuana
        fields = [
            'id', 'numero_registro', 'fecha_incautacion', 'cantidad_unidades',
            'departamento_nombre', 'direccion_policial_sigla', 'tipo_intervencion'
        ]


class PlantillaKgPBCListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listados de KG PBC
    """
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    direccion_policial_sigla = serializers.CharField(source='direccion_policial.sigla', read_only=True)
    
    class Meta:
        model = PlantillaKgPBC
        fields = [
            'id', 'numero_registro', 'fecha_incautacion', 'cantidad_kilogramos',
            'departamento_nombre', 'direccion_policial_sigla', 'tipo_intervencion'
        ]


class PlantillaKgCCListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listados de KG CC
    """
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    direccion_policial_sigla = serializers.CharField(source='direccion_policial.sigla', read_only=True)
    
    class Meta:
        model = PlantillaKgCC
        fields = [
            'id', 'numero_registro', 'fecha_incautacion', 'cantidad_kilogramos',
            'departamento_nombre', 'direccion_policial_sigla', 'tipo_intervencion'
        ]


class PlantillaKgMarihuanaListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listados de KG MARIHUANA
    """
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    direccion_policial_sigla = serializers.CharField(source='direccion_policial.sigla', read_only=True)
    
    class Meta:
        model = PlantillaKgMarihuana
        fields = [
            'id', 'numero_registro', 'fecha_incautacion', 'cantidad_kilogramos',
            'departamento_nombre', 'direccion_policial_sigla', 'tipo_intervencion'
        ]


class PlantillaKgLatexOpioListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listados de KG LÁTEX OPIO
    """
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    direccion_policial_sigla = serializers.CharField(source='direccion_policial.sigla', read_only=True)
    
    class Meta:
        model = PlantillaKgLatexOpio
        fields = [
            'id', 'numero_registro', 'fecha_incautacion', 'cantidad_kilogramos',
            'departamento_nombre', 'direccion_policial_sigla', 'tipo_intervencion'
        ]


class PlantillaKgDrogaSinteticaListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listados de KG DROGA SINTÉTICA
    """
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    direccion_policial_sigla = serializers.CharField(source='direccion_policial.sigla', read_only=True)
    
    class Meta:
        model = PlantillaKgDrogaSintetica
        fields = [
            'id', 'numero_registro', 'fecha_incautacion', 'cantidad_kilogramos',
            'departamento_nombre', 'direccion_policial_sigla', 'tipo_intervencion'
        ]
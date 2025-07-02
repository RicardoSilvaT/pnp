from rest_framework import serializers
from production.models import (
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
    SituacionDetenido, Fiscalia
)


# =============================================================================
# SERIALIZERS DE UBICACIÓN GEOGRÁFICA
# =============================================================================

class DepartamentoSerializer(serializers.ModelSerializer):
    """Serializer para Departamentos"""
    
    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'codigo']
        read_only_fields = ['id']


class ProvinciaSerializer(serializers.ModelSerializer):
    """Serializer para Provincias"""
    departamento_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Provincia
        fields = ['id', 'nombre', 'codigo', 'departamento', 'departamento_data']
        read_only_fields = ['id']
    
    def get_departamento_data(self, obj):
        return {
            'id': obj.departamento.id,
            'nombre': obj.departamento.nombre,
            'codigo': obj.departamento.codigo
        }


class DistritoSerializer(serializers.ModelSerializer):
    """Serializer para Distritos"""
    provincia_data = serializers.SerializerMethodField()
    departamento_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Distrito
        fields = ['id', 'nombre', 'codigo', 'provincia', 'provincia_data', 'departamento_data']
        read_only_fields = ['id']
    
    def get_provincia_data(self, obj):
        return {
            'id': obj.provincia.id,
            'nombre': obj.provincia.nombre,
            'codigo': obj.provincia.codigo
        }
    
    def get_departamento_data(self, obj):
        return {
            'id': obj.provincia.departamento.id,
            'nombre': obj.provincia.departamento.nombre,
            'codigo': obj.provincia.departamento.codigo
        }


# =============================================================================
# SERIALIZERS DE DATOS DE PERSONAS
# =============================================================================

class NacionalidadSerializer(serializers.ModelSerializer):
    """Serializer para Nacionalidades"""
    
    class Meta:
        model = Nacionalidad
        fields = ['id', 'nombre', 'codigo']
        read_only_fields = ['id']


class TipoDocumentoSerializer(serializers.ModelSerializer):
    """Serializer para Tipos de Documento"""
    
    class Meta:
        model = TipoDocumento
        fields = ['id', 'nombre', 'codigo']
        read_only_fields = ['id']


class TipoRequisitoriaSerializer(serializers.ModelSerializer):
    """Serializer para Tipos de Requisitoria"""
    
    class Meta:
        model = TipoRequisitoria
        fields = ['id', 'nombre', 'descripcion']
        read_only_fields = ['id']


# =============================================================================
# SERIALIZERS DE DELITOS
# =============================================================================

class DelitoFueroSerializer(serializers.ModelSerializer):
    """Serializer para Delitos Fuero"""
    
    class Meta:
        model = DelitoFuero
        fields = ['id', 'nombre', 'descripcion']
        read_only_fields = ['id']


class DelitoGeneralSerializer(serializers.ModelSerializer):
    """Serializer para Delitos Generales"""
    delito_fuero_data = serializers.SerializerMethodField()
    
    class Meta:
        model = DelitoGeneral
        fields = ['id', 'nombre', 'descripcion', 'delito_fuero', 'delito_fuero_data']
        read_only_fields = ['id']
    
    def get_delito_fuero_data(self, obj):
        return {
            'id': obj.delito_fuero.id,
            'nombre': obj.delito_fuero.nombre
        }


class DelitoEspecificoSerializer(serializers.ModelSerializer):
    """Serializer para Delitos Específicos"""
    delito_general_data = serializers.SerializerMethodField()
    delito_fuero_data = serializers.SerializerMethodField()
    
    class Meta:
        model = DelitoEspecifico
        fields = ['id', 'nombre', 'descripcion', 'delito_general', 'delito_general_data', 'delito_fuero_data']
        read_only_fields = ['id']
    
    def get_delito_general_data(self, obj):
        return {
            'id': obj.delito_general.id,
            'nombre': obj.delito_general.nombre
        }
    
    def get_delito_fuero_data(self, obj):
        return {
            'id': obj.delito_general.delito_fuero.id,
            'nombre': obj.delito_general.delito_fuero.nombre
        }


class DelitoSubtipoSerializer(serializers.ModelSerializer):
    """Serializer para Delitos Subtipos"""
    delito_especifico_data = serializers.SerializerMethodField()
    delito_general_data = serializers.SerializerMethodField()
    delito_fuero_data = serializers.SerializerMethodField()
    
    class Meta:
        model = DelitoSubtipo
        fields = [
            'id', 'nombre', 'descripcion', 'delito_especifico',
            'delito_especifico_data', 'delito_general_data', 'delito_fuero_data'
        ]
        read_only_fields = ['id']
    
    def get_delito_especifico_data(self, obj):
        return {
            'id': obj.delito_especifico.id,
            'nombre': obj.delito_especifico.nombre
        }
    
    def get_delito_general_data(self, obj):
        return {
            'id': obj.delito_especifico.delito_general.id,
            'nombre': obj.delito_especifico.delito_general.nombre
        }
    
    def get_delito_fuero_data(self, obj):
        return {
            'id': obj.delito_especifico.delito_general.delito_fuero.id,
            'nombre': obj.delito_especifico.delito_general.delito_fuero.nombre
        }


# =============================================================================
# SERIALIZERS DE ESTRUCTURA POLICIAL
# =============================================================================

class DireccionPolicialSerializer(serializers.ModelSerializer):
    """Serializer para Direcciones Policiales"""
    
    class Meta:
        model = DireccionPolicial
        fields = ['id', 'nombre', 'sigla', 'descripcion']
        read_only_fields = ['id']


class DireccionEspecializadaSerializer(serializers.ModelSerializer):
    """Serializer para Direcciones Especializadas"""
    direccion_policial_data = serializers.SerializerMethodField()
    
    class Meta:
        model = DireccionEspecializada
        fields = ['id', 'nombre', 'sigla', 'descripcion', 'direccion_policial', 'direccion_policial_data']
        read_only_fields = ['id']
    
    def get_direccion_policial_data(self, obj):
        return {
            'id': obj.direccion_policial.id,
            'nombre': obj.direccion_policial.nombre,
            'sigla': obj.direccion_policial.sigla
        }


class DivisionPolicialSerializer(serializers.ModelSerializer):
    """Serializer para Divisiones Policiales"""
    
    class Meta:
        model = DivisionPolicial
        fields = ['id', 'nombre', 'sigla', 'descripcion']
        read_only_fields = ['id']


class DepartamentoPolicialSerializer(serializers.ModelSerializer):
    """Serializer para Departamentos Policiales"""
    
    class Meta:
        model = DepartamentoPolicial
        fields = ['id', 'nombre', 'sigla', 'descripcion']
        read_only_fields = ['id']


class UnidadPolicialSerializer(serializers.ModelSerializer):
    """Serializer para Unidades Policiales"""
    
    class Meta:
        model = UnidadPolicial
        fields = ['id', 'nombre', 'sigla', 'descripcion']
        read_only_fields = ['id']


# =============================================================================
# SERIALIZERS DE ARMAS
# =============================================================================

class CategoriaArmaSerializer(serializers.ModelSerializer):
    """Serializer para Categorías de Armas"""
    
    class Meta:
        model = CategoriaArma
        fields = ['id', 'nombre', 'descripcion']
        read_only_fields = ['id']


class TipoArmaSerializer(serializers.ModelSerializer):
    """Serializer para Tipos de Armas"""
    categoria_arma_data = serializers.SerializerMethodField()
    
    class Meta:
        model = TipoArma
        fields = ['id', 'nombre', 'descripcion', 'categoria_arma', 'categoria_arma_data']
        read_only_fields = ['id']
    
    def get_categoria_arma_data(self, obj):
        return {
            'id': obj.categoria_arma.id,
            'nombre': obj.categoria_arma.nombre
        }


# =============================================================================
# SERIALIZERS JUDICIALES
# =============================================================================

class SituacionDetenidoSerializer(serializers.ModelSerializer):
    """Serializer para Situaciones del Detenido"""
    
    class Meta:
        model = SituacionDetenido
        fields = ['id', 'nombre', 'descripcion']
        read_only_fields = ['id']


class FiscaliaSerializer(serializers.ModelSerializer):
    """Serializer para Fiscalías"""
    departamento_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Fiscalia
        fields = ['id', 'nombre', 'direccion', 'telefono', 'departamento', 'departamento_data']
        read_only_fields = ['id']
    
    def get_departamento_data(self, obj):
        if obj.departamento:
            return {
                'id': obj.departamento.id,
                'nombre': obj.departamento.nombre,
                'codigo': obj.departamento.codigo
            }
        return None


# =============================================================================
# SERIALIZERS PARA FILTROS Y OPCIONES
# =============================================================================

class ProvinciasPorDepartamentoSerializer(serializers.ModelSerializer):
    """Serializer para obtener provincias filtradas por departamento"""
    
    class Meta:
        model = Provincia
        fields = ['id', 'nombre', 'codigo']


class DistritosPorProvinciaSerializer(serializers.ModelSerializer):
    """Serializer para obtener distritos filtrados por provincia"""
    
    class Meta:
        model = Distrito
        fields = ['id', 'nombre', 'codigo']


class DelitosGeneralesPorFueroSerializer(serializers.ModelSerializer):
    """Serializer para obtener delitos generales filtrados por fuero"""
    
    class Meta:
        model = DelitoGeneral
        fields = ['id', 'nombre', 'descripcion']


class DelitosEspecificosPorGeneralSerializer(serializers.ModelSerializer):
    """Serializer para obtener delitos específicos filtrados por general"""
    
    class Meta:
        model = DelitoEspecifico
        fields = ['id', 'nombre', 'descripcion']


class DelitosSubtiposPorEspecificoSerializer(serializers.ModelSerializer):
    """Serializer para obtener delitos subtipos filtrados por específico"""
    
    class Meta:
        model = DelitoSubtipo
        fields = ['id', 'nombre', 'descripcion']


class DireccionesEspecializadasPorDireccionSerializer(serializers.ModelSerializer):
    """Serializer para obtener direcciones especializadas filtradas por dirección policial"""
    
    class Meta:
        model = DireccionEspecializada
        fields = ['id', 'nombre', 'sigla', 'descripcion']


class TiposArmaPorCategoriaSerializer(serializers.ModelSerializer):
    """Serializer para obtener tipos de arma filtrados por categoría"""
    
    class Meta:
        model = TipoArma
        fields = ['id', 'nombre', 'descripcion']
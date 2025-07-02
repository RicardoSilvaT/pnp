from rest_framework import serializers
from .models import (
    Plantilla, CampoPlantilla, Departamento, Provincia, Distrito,
    TipoDocumento, DelitoGeneral, DelitoEspecifico, SubTipoDelito,
    SubmisionFormulario, DatosDetenido, LugarDetencion, DatosDelito,
    DatosUnidad, DatosRequisitoria, DatosDetencion
)


# ======================================
# SERIALIZERS DE CATÁLOGOS
# ======================================


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = ['id', 'nombre', 'codigo']


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'codigo']


class ProvinciaSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
   
    class Meta:
        model = Provincia
        fields = ['id', 'nombre', 'codigo', 'departamento', 'departamento_nombre']


class DistritoSerializer(serializers.ModelSerializer):
    provincia_nombre = serializers.CharField(source='provincia.nombre', read_only=True)
    departamento_nombre = serializers.CharField(source='provincia.departamento.nombre', read_only=True)
   
    class Meta:
        model = Distrito
        fields = ['id', 'nombre', 'codigo', 'provincia', 'provincia_nombre', 'departamento_nombre']


class SubTipoDelitoSerializer(serializers.ModelSerializer):
    delito_especifico_nombre = serializers.CharField(source='delito_especifico.nombre', read_only=True)
    delito_general_nombre = serializers.CharField(source='delito_especifico.delito_general.nombre', read_only=True)
   
    class Meta:
        model = SubTipoDelito
        fields = [
            'id', 'nombre', 'codigo', 'delito_especifico',
            'delito_especifico_nombre', 'delito_general_nombre'
        ]


class DelitoEspecificoSerializer(serializers.ModelSerializer):
    delito_general_nombre = serializers.CharField(source='delito_general.nombre', read_only=True)
    sub_tipos = SubTipoDelitoSerializer(many=True, read_only=True)
   
    class Meta:
        model = DelitoEspecifico
        fields = ['id', 'nombre', 'codigo', 'delito_general', 'delito_general_nombre', 'sub_tipos']


class DelitoGeneralSerializer(serializers.ModelSerializer):
    delitos_especificos = DelitoEspecificoSerializer(many=True, read_only=True)
   
    class Meta:
        model = DelitoGeneral
        fields = ['id', 'nombre', 'codigo', 'delitos_especificos']


# ======================================
# SERIALIZERS DE PLANTILLAS Y CAMPOS
# ======================================


class CampoPlantillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampoPlantilla
        fields = [
            'id', 'nombre_campo', 'etiqueta_campo', 'tipo_campo',
            'requerido', 'orden_campo', 'opciones', 'grupo_campo'
        ]


class PlantillaSerializer(serializers.ModelSerializer):
    campos = CampoPlantillaSerializer(many=True, read_only=True)
    total_campos = serializers.SerializerMethodField()
   
    class Meta:
        model = Plantilla
        fields = ['id', 'nombre', 'descripcion', 'activo', 'fecha_creacion', 'campos', 'total_campos']
   
    def get_total_campos(self, obj):
        return obj.campos.count()


class PlantillaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de plantillas"""
    total_campos = serializers.SerializerMethodField()
   
    class Meta:
        model = Plantilla
        fields = ['id', 'nombre', 'descripcion', 'activo', 'total_campos']
   
    def get_total_campos(self, obj):
        return obj.campos.count()


# ======================================
# SERIALIZERS DE DATOS ESPECÍFICOS
# ======================================


class DatosDetenidoSerializer(serializers.ModelSerializer):
    tipo_documento_nombre = serializers.CharField(source='tipo_documento.nombre', read_only=True)
   
    class Meta:
        model = DatosDetenido
        fields = [
            'id', 'apellido_paterno', 'apellido_materno', 'nombres',
            'edad', 'genero', 'tipo_documento', 'tipo_documento_nombre',
            'numero_documento', 'nacionalidad'
        ]


class LugarDetencionSerializer(serializers.ModelSerializer):
    distrito_nombre = serializers.CharField(source='distrito.nombre', read_only=True)
    provincia_nombre = serializers.CharField(source='distrito.provincia.nombre', read_only=True)
    departamento_nombre = serializers.CharField(source='distrito.provincia.departamento.nombre', read_only=True)
   
    class Meta:
        model = LugarDetencion
        fields = [
            'id', 'distrito', 'distrito_nombre',
            'provincia_nombre', 'departamento_nombre'
        ]


class DatosDelitoSerializer(serializers.ModelSerializer):
    sub_tipo_delito_nombre = serializers.CharField(source='sub_tipo_delito.nombre', read_only=True)
    delito_especifico_nombre = serializers.CharField(source='sub_tipo_delito.delito_especifico.nombre', read_only=True)
    delito_general_nombre = serializers.CharField(source='sub_tipo_delito.delito_especifico.delito_general.nombre', read_only=True)
   
    class Meta:
        model = DatosDelito
        fields = [
            'id', 'sub_tipo_delito', 'sub_tipo_delito_nombre',
            'delito_especifico_nombre', 'delito_general_nombre',
            'multiples_delitos', 'otros_delitos'
        ]


class DatosUnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosUnidad
        fields = [
            'id', 'direccion_especializada', 'division_policial',
            'departamento_policial', 'nombre_unidad'
        ]


class DatosRequisitoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosRequisitoria
        fields = ['id', 'autoridad_orden_captura', 'pertenece_mas_buscados']


class DatosDetencionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosDetencion
        fields = ['id', 'motivo_detencion']


# ======================================
# SERIALIZER PRINCIPAL DE FORMULARIO
# ======================================


class SubmisionFormularioSerializer(serializers.ModelSerializer):
    plantilla = serializers.PrimaryKeyRelatedField(read_only=True) #FIX ERROR DONE
    plantilla_nombre = serializers.CharField(source='plantilla.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    datos_detenido = DatosDetenidoSerializer(read_only=True)
    lugar_detencion = LugarDetencionSerializer(read_only=True)
    datos_delito = DatosDelitoSerializer(many=True, read_only=True)
    datos_unidad = DatosUnidadSerializer(read_only=True)
    datos_requisitoria = DatosRequisitoriaSerializer(read_only=True)
    datos_detencion = DatosDetencionSerializer(read_only=True)
   
    class Meta:
        model = SubmisionFormulario
        fields = [
            'id', 'numero_formulario', 'plantilla', 'plantilla_nombre',
            'usuario', 'usuario_nombre', 'fecha_detencion', 'hora_detencion',
            'nota_informativa_sicpip', 'estado', 'fecha_creacion', 'fecha_actualizacion',
            'datos_detenido', 'lugar_detencion', 'datos_delito', 'datos_unidad',
            'datos_requisitoria', 'datos_detencion'
        ]
        read_only_fields = ['numero_formulario', 'fecha_creacion', 'fecha_actualizacion']


class SubmisionFormularioListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de formularios"""
    plantilla_nombre = serializers.CharField(source='plantilla.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    detenido_nombre = serializers.SerializerMethodField()
   
    class Meta:
        model = SubmisionFormulario
        fields = [
            'id', 'numero_formulario', 'plantilla_nombre', 'usuario_nombre',
            'fecha_detencion', 'estado', 'fecha_creacion', 'detenido_nombre'
        ]
   
    def get_detenido_nombre(self, obj):
        try:
            detenido = obj.datos_detenido
            return f"{detenido.apellido_paterno} {detenido.apellido_materno}, {detenido.nombres}"
        except:
            return "Sin datos"


# ======================================
# SERIALIZER PARA CREAR FORMULARIO COMPLETO - CORREGIDO
# ======================================


class CrearFormularioCompletoSerializer(serializers.Serializer):
    """Serializer para crear un formulario completo con todos sus datos relacionados"""
   
    # Datos principales
    plantilla = serializers.IntegerField() 
    numero = serializers.CharField(max_length=50, required=False)  # AGREGADO: Campo número de la plantilla
    fecha_detencion = serializers.DateField()
    hora_detencion = serializers.TimeField()
    nota_informativa = serializers.CharField(required=False, allow_blank=True)  # CORREGIDO: era nota_informativa_sicpip
   
    # Datos del detenido
    apellido_paterno = serializers.CharField(max_length=100)
    apellido_materno = serializers.CharField(max_length=100)
    nombres = serializers.CharField(max_length=150)
    edad = serializers.IntegerField(min_value=0, max_value=120)
    genero = serializers.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino')])
    tipo_documento = serializers.IntegerField()
    numero_documento = serializers.CharField(max_length=20)
    nacionalidad = serializers.CharField(max_length=100, default='Peruana')
   
    # Lugar de detención - AGREGADOS departamento y provincia para cascada
    departamento = serializers.IntegerField(required=False)  # AGREGADO: Para cascada frontend
    provincia = serializers.IntegerField(required=False)     # AGREGADO: Para cascada frontend
    distrito = serializers.IntegerField()
   
    # Delito - AGREGADOS para cascada
    delito_general = serializers.IntegerField(required=False)    # AGREGADO: Para cascada frontend
    delito_especifico = serializers.IntegerField(required=False) # AGREGADO: Para cascada frontend
    sub_tipo = serializers.IntegerField()  # CORREGIDO: era sub_tipo_delito
    multiples_delitos = serializers.BooleanField(default=False)
    otros_delitos = serializers.CharField(required=False, allow_blank=True)
   
    # Datos de la unidad
    direccion_especializada = serializers.CharField(max_length=200)
    division_policial = serializers.CharField(max_length=200)
    departamento_policial = serializers.CharField(max_length=200)
    nombre_unidad = serializers.CharField(max_length=200)
   
    # Campos específicos opcionales
    autoridad_orden_captura = serializers.CharField(max_length=200, required=False)
    pertenece_mas_buscados = serializers.BooleanField(required=False)
    motivo_detencion = serializers.ChoiceField(
        choices=[('flagrancia', 'Flagrancia'), ('detencion_preliminar', 'Detención Preliminar')],
        required=False
    )
   
    def create(self, validated_data):
        from django.db import transaction
        import uuid
       
        # Extraer datos por secciones
        plantilla_id = validated_data.pop('plantilla')
        
        # Extraer campos de cascada (no se guardan, solo para frontend)
        validated_data.pop('departamento', None)  # AGREGADO: Remover cascada
        validated_data.pop('provincia', None)     # AGREGADO: Remover cascada
        validated_data.pop('delito_general', None)    # AGREGADO: Remover cascada
        validated_data.pop('delito_especifico', None) # AGREGADO: Remover cascada
        validated_data.pop('numero', None)  # AGREGADO: Remover número (se genera automático)
       
        # Datos del detenido
        datos_detenido = {
            'apellido_paterno': validated_data.pop('apellido_paterno'),
            'apellido_materno': validated_data.pop('apellido_materno'),
            'nombres': validated_data.pop('nombres'),
            'edad': validated_data.pop('edad'),
            'genero': validated_data.pop('genero'),
            'tipo_documento_id': validated_data.pop('tipo_documento'),
            'numero_documento': validated_data.pop('numero_documento'),
            'nacionalidad': validated_data.pop('nacionalidad'),
        }
       
        # Lugar de detención
        distrito_id = validated_data.pop('distrito')
       
        # Delito
        datos_delito = {
            'sub_tipo_delito_id': validated_data.pop('sub_tipo'),  # CORREGIDO: mapear sub_tipo a sub_tipo_delito_id
            'multiples_delitos': validated_data.pop('multiples_delitos'),
            'otros_delitos': validated_data.pop('otros_delitos', ''),
        }
       
        # Datos de la unidad
        datos_unidad = {
            'direccion_especializada': validated_data.pop('direccion_especializada'),
            'division_policial': validated_data.pop('division_policial'),
            'departamento_policial': validated_data.pop('departamento_policial'),
            'nombre_unidad': validated_data.pop('nombre_unidad'),
        }
       
        # Datos específicos
        autoridad_orden_captura = validated_data.pop('autoridad_orden_captura', None)
        pertenece_mas_buscados = validated_data.pop('pertenece_mas_buscados', None)
        motivo_detencion = validated_data.pop('motivo_detencion', None)
       
        with transaction.atomic():
            # Crear formulario principal
            plantilla = Plantilla.objects.get(id=plantilla_id)
            numero_formulario = f"{plantilla.nombre}-{uuid.uuid4().hex[:8].upper()}"
           
            formulario = SubmisionFormulario.objects.create(
                plantilla=plantilla,
                usuario=self.context['request'].user,
                numero_formulario=numero_formulario,
                nota_informativa_sicpip=validated_data.pop('nota_informativa', ''),  # CORREGIDO: mapear nota_informativa
                **validated_data
            )
           
            # Crear datos relacionados
            DatosDetenido.objects.create(submision_formulario=formulario, **datos_detenido)
            LugarDetencion.objects.create(submision_formulario=formulario, distrito_id=distrito_id)
            DatosDelito.objects.create(submision_formulario=formulario, **datos_delito)
            DatosUnidad.objects.create(submision_formulario=formulario, **datos_unidad)
           
            # Crear datos específicos según plantilla
            if plantilla.nombre == "RQ" and autoridad_orden_captura:
                DatosRequisitoria.objects.create(
                    submision_formulario=formulario,
                    autoridad_orden_captura=autoridad_orden_captura,
                    pertenece_mas_buscados=pertenece_mas_buscados or False
                )
           
            if plantilla.nombre in ["Diversos Delitos", "Menores"] and motivo_detencion:
                DatosDetencion.objects.create(
                    submision_formulario=formulario,
                    motivo_detencion=motivo_detencion
                )
           
            return formulario


# ======================================
# SERIALIZERS DE UBICACIÓN JERÁRQUICA
# ======================================


class UbicacionJerarquicaSerializer(serializers.Serializer):
    """Serializer para obtener ubicaciones organizadas jerárquicamente"""
    departamentos = DepartamentoSerializer(many=True)
    provincias = ProvinciaSerializer(many=True)
    distritos = DistritoSerializer(many=True)
from rest_framework import serializers
from .models import ViolenciaFamiliar, RegistroCarga

class ViolenciaFamiliarSerializer(serializers.ModelSerializer):
    # Muestra el ID del lote de importación
    carga = serializers.PrimaryKeyRelatedField(read_only=True)
    # Información adicional de auditoría
    creado_por = serializers.CharField(source='carga.usuario.username', read_only=True)
    fecha_carga = serializers.DateTimeField(source='carga.creado_en', read_only=True)

    class Meta:
        model = ViolenciaFamiliar
        # Incluye todos los campos del modelo y los campos de auditoría
        fields = [
            'id', 'id_doc_denuncia', 'libro', 'num_denuncia', 'tipodenuncia', 'situaciondenuncia',
            'tipo', 'subtipo', 'modalidad', 'fec_hecho_fecha', 'fec_hecho_hora',
            'dpto', 'prov', 'distrito', 'tipovia', 'ubicacion', 'cuadra', 'dni',
            'apellido_paterno', 'apellido_materno', 'nombre', 'situacionpersona',
            'fec_nacimiento_fecha', 'fec_nacimiento_hora', 'edad', 'sexo', 'estadocivil',
            'gradoinstruccion', 'ocupacion', 'pais_natal', 'region', 'descripcioncomisaria',
            'fec_registro_fecha', 'fec_registro_hora', 'xx', 'yy',
            # Campos de auditoría
            'carga', 'creado_por', 'fecha_carga'
        ]

# Serializador para los lotes de carga, en caso de necesitarlo
class RegistroCargaSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source='usuario.username', read_only=True)
    class Meta:
        model = RegistroCarga
        fields = ['id', 'usuario', 'creado_en']

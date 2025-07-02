import json
import math
import pandas as pd
from rest_framework import status
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import ViolenciaFamiliar, RegistroCarga
from .serializers import ViolenciaFamiliarSerializer


def sanitize_json(data):
    def clean_value(val):
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return None
        return val

    if isinstance(data, list):
        return [{k: clean_value(v) for k, v in d.items()} for d in data]
    elif isinstance(data, dict):
        return {k: clean_value(v) for k, v in data.items()}
    return data


def limpio(val):
    return "" if pd.isna(val) or val is None else str(val)


def limpio_int(val):
    return int(val) if pd.notnull(val) else 0


def limpio_float(val):
    return float(val) if pd.notnull(val) else 0.0


def convertir_fecha_segura(valor):
    try:
        fecha = pd.to_datetime(valor, errors='coerce')
        return None if pd.isna(fecha) else fecha
    except Exception:
        return None


class UploadIncidenciasView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Crear registro de lote de importación
        carga = RegistroCarga.objects.create(usuario=request.user)

        file = request.FILES.get('file')
        df = pd.read_excel(file)

        df = df.applymap(lambda x: str(x).encode('utf-8').decode('utf-8') if isinstance(x, str) else x)
        df.columns = df.columns.str.strip().str.upper()
        df = df.where(pd.notnull(df), None)

        print("Columnas recibidas desde el Excel:", df.columns.tolist())

        columnas_obligatorias = [
            'ID_DOC_DENUNCIA', 'LIBRO', 'NUM_DENUNCIA', 'TIPODENUNCIA', 'SITUACIONDENUNCIA',
            'TIPO', 'SUBTIPO', 'MODALIDAD', 'FEC_HORA_HECHO', 'DPTO', 'PROV', 'DISTRITO',
            'TIPOVIA', 'UBICACION', 'CUADRA', 'DNI', 'APELLIDO_PATERNO', 'APELLIDO_MATERNO',
            'NOMBRE', 'SITUACIONPERSONA', 'FEC_NACIMIENTO', 'EDAD_PERSONA', 'SEXO',
            'ESTADOCIVIL', 'GRADOINSTRUCCION', 'OCUPACION', 'PAIS_NATAL', 'REGION',
            'DESCRIPCIONCOMISARIA', 'FEC_REGISTRO', 'XX', 'YY'
        ]
        faltantes = [col for col in columnas_obligatorias if col not in df.columns]
        if faltantes:
            return Response(
                {'error': 'El archivo Excel no contiene todas las columnas requeridas.',
                 'faltantes': faltantes,
                 'recibidas': df.columns.tolist()},
                status=status.HTTP_400_BAD_REQUEST
            )

        nuevas_incidencias = []
        for index, row in df.iterrows():
            try:
                print(f"[DEBUG] Procesando fila {index + 2}")
                row = row.where(pd.notnull(row), None)

                hecho_dt = convertir_fecha_segura(row['FEC_HORA_HECHO'])
                nacimiento_dt = convertir_fecha_segura(row['FEC_NACIMIENTO'])
                registro_dt = convertir_fecha_segura(row['FEC_REGISTRO'])

                incidencia = ViolenciaFamiliar.objects.create(
                    id_doc_denuncia=limpio_int(row['ID_DOC_DENUNCIA']),
                    libro=limpio(row['LIBRO']),
                    num_denuncia=limpio(row['NUM_DENUNCIA']),
                    tipodenuncia=limpio(row['TIPODENUNCIA']),
                    situaciondenuncia=limpio(row['SITUACIONDENUNCIA']),
                    tipo=limpio(row['TIPO']),
                    subtipo=limpio(row['SUBTIPO']),
                    modalidad=limpio(row['MODALIDAD']),
                    fec_hecho_fecha=hecho_dt.date() if hecho_dt else None,
                    fec_hecho_hora=hecho_dt.time() if hecho_dt else None,
                    dpto=limpio(row['DPTO']),
                    prov=limpio(row['PROV']),
                    distrito=limpio(row['DISTRITO']),
                    tipovia=limpio(row['TIPOVIA']),
                    ubicacion=limpio(row['UBICACION']),
                    cuadra=limpio(row['CUADRA']),
                    dni=limpio(row['DNI']),
                    apellido_paterno=limpio(row['APELLIDO_PATERNO']),
                    apellido_materno=limpio(row['APELLIDO_MATERNO']),
                    nombre=limpio(row['NOMBRE']),
                    situacionpersona=limpio(row['SITUACIONPERSONA']),
                    fec_nacimiento_fecha=nacimiento_dt.date() if nacimiento_dt else None,
                    fec_nacimiento_hora=nacimiento_dt.time() if nacimiento_dt else None,
                    edad=limpio_int(row['EDAD_PERSONA']),
                    sexo=limpio(row['SEXO']),
                    estadocivil=limpio(row['ESTADOCIVIL']),
                    gradoinstruccion=limpio(row['GRADOINSTRUCCION']),
                    ocupacion=limpio(row['OCUPACION']),
                    pais_natal=limpio(row['PAIS_NATAL']),
                    region=limpio(row['REGION']),
                    descripcioncomisaria=limpio(row['DESCRIPCIONCOMISARIA']),
                    fec_registro_fecha=registro_dt.date() if registro_dt else None,
                    fec_registro_hora=registro_dt.time() if registro_dt else None,
                    xx=limpio_float(row['XX']),
                    yy=limpio_float(row['YY']),
                    carga=carga
                )
                nuevas_incidencias.append(incidencia)

            except Exception as e:
                print(f"[ADVERTENCIA] Error al guardar fila {index + 2}: {e}")
                continue

        if not nuevas_incidencias:
            return Response({'error': 'No se pudo guardar ninguna fila del archivo.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ViolenciaFamiliarSerializer(nuevas_incidencias, many=True)
        datos_serializados = sanitize_json(serializer.data)
        return Response({'mensaje': 'Datos cargados correctamente', 'datos': datos_serializados})


class ListarIncidenciasView(ListAPIView):
    queryset = ViolenciaFamiliar.objects.all()
    serializer_class = ViolenciaFamiliarSerializer


class DeleteBatchIncidenciasView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        ids = request.data.get('ids', [])
        if not isinstance(ids, list) or not ids:
            return Response({'error': 'Debes enviar una lista de IDs para eliminar.'}, status=status.HTTP_400_BAD_REQUEST)
        borrados, _ = ViolenciaFamiliar.objects.filter(id__in=ids).delete()
        return Response({'mensaje': f'Se eliminaron {borrados} registros correctamente.'}, status=status.HTTP_200_OK)

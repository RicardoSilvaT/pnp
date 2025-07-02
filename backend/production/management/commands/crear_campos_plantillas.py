from django.core.management.base import BaseCommand
from production.models import Plantilla, CampoPlantilla


class Command(BaseCommand):
    help = 'Crear campos para todas las plantillas del sistema'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Iniciando creación de campos para plantillas...')
        
        try:
            # Obtener las plantillas
            rq = Plantilla.objects.get(nombre="RQ")
            diversos = Plantilla.objects.get(nombre="Diversos Delitos")
            menores = Plantilla.objects.get(nombre="Menores")
            
            self.stdout.write('✅ Plantillas encontradas correctamente')
            
            # ======================================
            # CAMPOS COMUNES A TODAS LAS PLANTILLAS
            # ======================================
            
            campos_comunes = [
                # Datos Generales
                {
                    'nombre_campo': 'numero',
                    'etiqueta_campo': 'N°',
                    'tipo_campo': 'text',
                    'requerido': True,
                    'orden_campo': 1,
                    'grupo_campo': 'datos_generales'
                },
                {
                    'nombre_campo': 'fecha_detencion',
                    'etiqueta_campo': 'SELECCIONAR FECHA DE DETENCIÓN',
                    'tipo_campo': 'date',
                    'requerido': True,
                    'orden_campo': 2,
                    'grupo_campo': 'datos_generales'
                },
                {
                    'nombre_campo': 'hora_detencion',
                    'etiqueta_campo': 'REGISTRAR HORA DETENCIÓN',
                    'tipo_campo': 'time',
                    'requerido': True,
                    'orden_campo': 3,
                    'grupo_campo': 'datos_generales'
                },
                
                # Datos del Detenido
                {
                    'nombre_campo': 'apellido_paterno',
                    'etiqueta_campo': 'REGISTRAR APELLIDO PATERNO',
                    'tipo_campo': 'text',
                    'requerido': True,
                    'orden_campo': 4,
                    'grupo_campo': 'datos_detenido'
                },
                {
                    'nombre_campo': 'apellido_materno',
                    'etiqueta_campo': 'REGISTRAR APELLIDO MATERNO',
                    'tipo_campo': 'text',
                    'requerido': True,
                    'orden_campo': 5,
                    'grupo_campo': 'datos_detenido'
                },
                {
                    'nombre_campo': 'nombres',
                    'etiqueta_campo': 'REGISTRAR NOMBRES',
                    'tipo_campo': 'text',
                    'requerido': True,
                    'orden_campo': 6,
                    'grupo_campo': 'datos_detenido'
                },
                {
                    'nombre_campo': 'edad',
                    'etiqueta_campo': 'REGISTRAR EDAD',
                    'tipo_campo': 'number',
                    'requerido': True,
                    'orden_campo': 7,
                    'grupo_campo': 'datos_detenido',
                    'opciones': {'min': 0, 'max': 120}
                },
                {
                    'nombre_campo': 'genero',
                    'etiqueta_campo': 'REGISTRAR GÉNERO',
                    'tipo_campo': 'select',
                    'requerido': True,
                    'orden_campo': 8,
                    'grupo_campo': 'datos_detenido',
                    'opciones': {
                        'valores': [
                            {'id': 'M', 'texto': 'Masculino'},
                            {'id': 'F', 'texto': 'Femenino'}
                        ]
                    }
                },
                {
                    'nombre_campo': 'tipo_documento',
                    'etiqueta_campo': 'TIPO DE DOCUMENTO',
                    'tipo_campo': 'select',
                    'requerido': True,
                    'orden_campo': 9,
                    'grupo_campo': 'datos_detenido',
                    'opciones': {
                        'valores': [
                            {'id': 1, 'texto': 'DNI'},
                            {'id': 2, 'texto': 'Carné de Extranjería'},
                            {'id': 3, 'texto': 'Pasaporte'},
                            {'id': 4, 'texto': 'Cédula de Identidad'}
                        ]
                    }
                },
                {
                    'nombre_campo': 'numero_documento',
                    'etiqueta_campo': 'REGISTRAR N° DE DOCUMENTO',
                    'tipo_campo': 'text',
                    'requerido': True,
                    'orden_campo': 10,
                    'grupo_campo': 'datos_detenido'
                },
                {
                    'nombre_campo': 'nacionalidad',
                    'etiqueta_campo': 'NACIONALIDAD (PAÍS)',
                    'tipo_campo': 'text',
                    'requerido': True,
                    'orden_campo': 11,
                    'grupo_campo': 'datos_detenido'
                },
                
                # Lugar de Detención
                {
                    'nombre_campo': 'departamento',
                    'etiqueta_campo': 'DEPARTAMENTO',
                    'tipo_campo': 'select',
                    'requerido': True,
                    'orden_campo': 12,
                    'grupo_campo': 'lugar_detencion'
                },
                {
                    'nombre_campo': 'provincia',
                    'etiqueta_campo': 'PROVINCIA',
                    'tipo_campo': 'select',
                    'requerido': True,
                    'orden_campo': 13,
                    'grupo_campo': 'lugar_detencion'
                },
                {
                    'nombre_campo': 'distrito',
                    'etiqueta_campo': 'DISTRITO',
                    'tipo_campo': 'select',
                    'requerido': True,
                    'orden_campo': 14,
                    'grupo_campo': 'lugar_detencion'
                },
                
                # Delito Cometido
                {
                    'nombre_campo': 'delito_general',
                    'etiqueta_campo': 'DELITO GENERAL',
                    'tipo_campo': 'select',
                    'requerido': True,
                    'orden_campo': 15,
                    'grupo_campo': 'delito_cometido'
                },
                {
                    'nombre_campo': 'delito_especifico',
                    'etiqueta_campo': 'DELITO ESPECÍFICO',
                    'tipo_campo': 'select',
                    'requerido': True,
                    'orden_campo': 16,
                    'grupo_campo': 'delito_cometido'
                },
                {
                    'nombre_campo': 'sub_tipo',
                    'etiqueta_campo': 'SUB TIPO',
                    'tipo_campo': 'select',
                    'requerido': True,
                    'orden_campo': 17,
                    'grupo_campo': 'delito_cometido'
                },
                {
                    'nombre_campo': 'otros_delitos',
                    'etiqueta_campo': 'REGISTRAR SI ES DETENIDO POR MÁS DE UN DELITO DEBERÁ INDICAR LOS OTROS DELITOS',
                    'tipo_campo': 'textarea',
                    'requerido': False,
                    'orden_campo': 18,
                    'grupo_campo': 'delito_cometido',
                    'opciones': {'filas': 3}
                },
                
                # Datos de la Unidad
                {
                    'nombre_campo': 'direccion_especializada',
                    'etiqueta_campo': 'DIRECCIÓN ESPECIALIZADAS/REGIÓN/FRENTE POLICIAL',
                    'tipo_campo': 'text',
                    'requerido': True,
                    'orden_campo': 19,
                    'grupo_campo': 'datos_unidad'
                },
                {
                    'nombre_campo': 'division_policial',
                    'etiqueta_campo': 'DIVISIÓN POLICIAL',
                    'tipo_campo': 'text',
                    'requerido': True,
                    'orden_campo': 20,
                    'grupo_campo': 'datos_unidad'
                },
                {
                    'nombre_campo': 'departamento_policial',
                    'etiqueta_campo': 'DEPARTAMENTO POLICIAL',
                    'tipo_campo': 'text',
                    'requerido': True,
                    'orden_campo': 21,
                    'grupo_campo': 'datos_unidad'
                },
                {
                    'nombre_campo': 'nombre_unidad',
                    'etiqueta_campo': 'EL NOMBRE DE LA UNIDAD/ÁREAS/EQUIPO',
                    'tipo_campo': 'text',
                    'requerido': True,
                    'orden_campo': 22,
                    'grupo_campo': 'datos_unidad'
                },
                {
                    'nombre_campo': 'nota_informativa',
                    'etiqueta_campo': 'REGISTRAR NOTA INFORMATIVA SICPIP',
                    'tipo_campo': 'textarea',
                    'requerido': False,
                    'orden_campo': 23,
                    'grupo_campo': 'otros',
                    'opciones': {'filas': 4}
                }
            ]
            
            # Crear campos comunes para todas las plantillas
            self.stdout.write('📝 Creando campos comunes...')
            for plantilla in [rq, diversos, menores]:
                for campo_data in campos_comunes:
                    CampoPlantilla.objects.create(
                        plantilla=plantilla,
                        **campo_data
                    )
            
            # ======================================
            # CAMPOS ESPECÍFICOS PARA RQ
            # ======================================
            
            self.stdout.write('🎯 Creando campos específicos para RQ...')
            campos_rq = [
                {
                    'nombre_campo': 'pertenece_mas_buscados',
                    'etiqueta_campo': 'EL REQUISITORIADO PERTENECE A LOS MÁS BUSCADOS (SI/NO)',
                    'tipo_campo': 'select',
                    'requerido': True,
                    'orden_campo': 24,
                    'grupo_campo': 'datos_detenido',
                    'opciones': {
                        'valores': [
                            {'id': True, 'texto': 'SÍ'},
                            {'id': False, 'texto': 'NO'}
                        ]
                    }
                },
                {
                    'nombre_campo': 'autoridad_orden_captura',
                    'etiqueta_campo': 'REGISTRAR LA AUTORIDAD QUE DISPONE LA ORDEN DE CAPTURA',
                    'tipo_campo': 'text',
                    'requerido': True,
                    'orden_campo': 25,
                    'grupo_campo': 'datos_requisitoria'
                }
            ]
            
            # Crear campos específicos para RQ
            for campo_data in campos_rq:
                CampoPlantilla.objects.create(
                    plantilla=rq,
                    **campo_data
                )
            
            # ======================================
            # CAMPOS ESPECÍFICOS PARA DIVERSOS DELITOS Y MENORES
            # ======================================
            
            self.stdout.write('🎯 Creando campos específicos para Diversos Delitos y Menores...')
            campo_motivo = {
                'nombre_campo': 'motivo_detencion',
                'etiqueta_campo': 'SELECCIONAR EL MOTIVO DE LA DETENCIÓN (FLAGRANCIA- DETENCIÓN PRELIMINAR)',
                'tipo_campo': 'select',
                'requerido': True,
                'orden_campo': 24,
                'grupo_campo': 'datos_detencion',
                'opciones': {
                    'valores': [
                        {'id': 'flagrancia', 'texto': 'Flagrancia'},
                        {'id': 'detencion_preliminar', 'texto': 'Detención Preliminar'}
                    ]
                }
            }
            
            # Crear campo motivo para Diversos Delitos y Menores
            for plantilla in [diversos, menores]:
                CampoPlantilla.objects.create(
                    plantilla=plantilla,
                    **campo_motivo
                )
            
            # Mostrar resumen
            self.stdout.write(
                self.style.SUCCESS("✅ Campos creados exitosamente para todas las plantillas!")
            )
            self.stdout.write(f"RQ: {CampoPlantilla.objects.filter(plantilla=rq).count()} campos")
            self.stdout.write(f"Diversos Delitos: {CampoPlantilla.objects.filter(plantilla=diversos).count()} campos")
            self.stdout.write(f"Menores: {CampoPlantilla.objects.filter(plantilla=menores).count()} campos")
            
        except Plantilla.DoesNotExist as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error: No se encontró alguna plantilla. {e}")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error inesperado: {e}")
            )
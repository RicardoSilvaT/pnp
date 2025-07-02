from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from production.models import PlantillaRQ, PlantillaDetenidos, PlantillaMenoresRetenidos
from production.serializers import (
    PlantillaRQSerializer, PlantillaDetenidosSerializer, PlantillaMenoresRetenidosSerializer
)
from .base_views import FormularioPersonasViewSet


# =============================================================================
# VIEWSETS PARA FORMULARIOS DE PERSONAS
# =============================================================================

class PlantillaRQViewSet(FormularioPersonasViewSet):
    """
    ViewSet para el formulario de Requisitorias (RQ)
    
    Endpoints disponibles:
    - GET /api/production/rq/ - Listar todas las RQ
    - POST /api/production/rq/ - Crear nueva RQ
    - GET /api/production/rq/{id}/ - Obtener RQ específica
    - PUT /api/production/rq/{id}/ - Actualizar RQ completa
    - PATCH /api/production/rq/{id}/ - Actualizar RQ parcial
    - DELETE /api/production/rq/{id}/ - Eliminar RQ
    - GET /api/production/rq/estadisticas/ - Estadísticas generales
    - GET /api/production/rq/estadisticas_personas/ - Estadísticas de personas
    - GET /api/production/rq/busqueda_avanzada/ - Búsqueda avanzada
    - GET /api/production/rq/reporte_resumen/ - Reporte resumen
    """
    queryset = PlantillaRQ.objects.select_related(
        'nacionalidad', 'tipo_documento', 'tipo_requisitoria',
        'departamento', 'provincia', 'distrito',
        'delito_fuero', 'delito_general', 'delito_especifico', 'delito_subtipo',
        'direccion_policial', 'direccion_especializada', 'division_policial',
        'departamento_policial', 'unidad_policial'
    ).all()
    
    serializer_class = PlantillaRQSerializer
    
    # Campos adicionales específicos para RQ
    filterset_fields = FormularioPersonasViewSet.filterset_fields + [
        'tipo_requisitoria', 'esta_en_lista_mas_buscados'
    ]
    
    search_fields = FormularioPersonasViewSet.search_fields + [
        'autoridad_que_solicita', 'documento_que_solicita'
    ]
    
    @action(detail=False, methods=['get'])
    def estadisticas_rq(self, request):
        """
        Estadísticas específicas para formularios RQ
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Estadísticas por tipo de requisitoria
        por_tipo_requisitoria = queryset.values(
            'tipo_requisitoria__nombre'
        ).annotate(
            total=Count('id')
        ).order_by('-total')
        
        # Estadísticas por lista de más buscados
        por_lista_buscados = queryset.values(
            'esta_en_lista_mas_buscados'
        ).annotate(
            total=Count('id')
        )
        
        # Estadísticas por funcionario público
        por_funcionario_publico = queryset.values(
            'es_funcionario_publico'
        ).annotate(
            total=Count('id')
        ).order_by('-total')
        
        return Response({
            'total_rq': queryset.count(),
            'por_tipo_requisitoria': list(por_tipo_requisitoria),
            'por_lista_mas_buscados': list(por_lista_buscados),
            'por_funcionario_publico': list(por_funcionario_publico)
        })
    
    @action(detail=False, methods=['get'])
    def buscar_por_documento(self, request):
        """
        Búsqueda específica por número de documento
        """
        numero_documento = request.query_params.get('numero_documento')
        
        if not numero_documento:
            return Response({
                'error': 'Se requiere el parámetro numero_documento'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar registros que coincidan
        resultados = self.get_queryset().filter(
            numero_documento__icontains=numero_documento
        )
        
        serializer = self.get_serializer(resultados, many=True)
        
        return Response({
            'total_encontrados': resultados.count(),
            'resultados': serializer.data
        })


class PlantillaDetenidosViewSet(FormularioPersonasViewSet):
    """
    ViewSet para el formulario de Detenidos por Diversos Delitos
    """
    queryset = PlantillaDetenidos.objects.select_related(
        'nacionalidad', 'tipo_documento',
        'departamento', 'provincia', 'distrito',
        'delito_fuero', 'delito_general', 'delito_especifico', 'delito_subtipo',
        'categoria_arma', 'tipo_arma', 'situacion_detenido', 'fiscalia',
        'direccion_policial', 'direccion_especializada', 'division_policial',
        'departamento_policial', 'unidad_policial'
    ).all()
    
    serializer_class = PlantillaDetenidosSerializer
    
    # Campos adicionales específicos para Detenidos
    filterset_fields = FormularioPersonasViewSet.filterset_fields + [
        'motivo_detencion', 'es_integrante_bbcc_oocc', 'categoria_arma', 
        'situacion_detenido', 'fiscalia'
    ]
    
    search_fields = FormularioPersonasViewSet.search_fields + [
        'nombre_bbcc_oocc', 'nombre_fiscal', 'vehiculo_implicado'
    ]
    
    @action(detail=False, methods=['get'])
    def estadisticas_detenidos(self, request):
        """
        Estadísticas específicas para formularios de Detenidos
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Estadísticas por motivo de detención
        por_motivo = queryset.values(
            'motivo_detencion'
        ).annotate(
            total=Count('id')
        )
        
        # Estadísticas por BBCC/OOCC
        por_bbcc_oocc = queryset.values(
            'es_integrante_bbcc_oocc'
        ).annotate(
            total=Count('id')
        )
        
        # Estadísticas por tipo de arma
        por_categoria_arma = queryset.filter(
            categoria_arma__isnull=False
        ).values(
            'categoria_arma__nombre'
        ).annotate(
            total=Count('id')
        ).order_by('-total')
        
        # Estadísticas por situación procesal
        por_situacion = queryset.filter(
            situacion_detenido__isnull=False
        ).values(
            'situacion_detenido__nombre'
        ).annotate(
            total=Count('id')
        ).order_by('-total')
        
        return Response({
            'total_detenidos': queryset.count(),
            'por_motivo_detencion': list(por_motivo),
            'por_bbcc_oocc': list(por_bbcc_oocc),
            'por_categoria_arma': list(por_categoria_arma),
            'por_situacion_procesal': list(por_situacion)
        })
    
    @action(detail=False, methods=['get'])
    def buscar_por_organizacion(self, request):
        """
        Búsqueda por nombre de organización criminal
        """
        nombre_organizacion = request.query_params.get('nombre_organizacion')
        
        if not nombre_organizacion:
            return Response({
                'error': 'Se requiere el parámetro nombre_organizacion'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar registros que coincidan
        resultados = self.get_queryset().filter(
            es_integrante_bbcc_oocc='SÍ',
            nombre_bbcc_oocc__icontains=nombre_organizacion
        )
        
        serializer = self.get_serializer(resultados, many=True)
        
        return Response({
            'total_encontrados': resultados.count(),
            'nombre_buscado': nombre_organizacion,
            'resultados': serializer.data
        })


class PlantillaMenoresRetenidosViewSet(FormularioPersonasViewSet):
    """
    ViewSet para el formulario de Menores Retenidos por Diversos Delitos
    """
    queryset = PlantillaMenoresRetenidos.objects.select_related(
        'nacionalidad', 'tipo_documento',
        'departamento', 'provincia', 'distrito',
        'delito_fuero', 'delito_general', 'delito_especifico', 'delito_subtipo',
        'categoria_arma', 'tipo_arma', 'situacion_detenido', 'fiscalia',
        'direccion_policial', 'direccion_especializada', 'division_policial',
        'departamento_policial', 'unidad_policial'
    ).all()
    
    serializer_class = PlantillaMenoresRetenidosSerializer
    
    # Campos específicos para Menores (sin funcionario público)
    filterset_fields = [
        'genero', 'edad', 'nacionalidad', 'tipo_documento',
        'departamento', 'provincia', 'distrito',
        'motivo_detencion', 'es_integrante_bbcc_oocc', 'categoria_arma', 
        'situacion_detenido', 'fiscalia', 'direccion_policial'
    ]
    
    search_fields = FormularioPersonasViewSet.search_fields + [
        'nombre_bbcc_oocc', 'nombre_fiscal'
    ]
    
    # Filtrar solo menores de edad en el queryset
    def get_queryset(self):
        return super().get_queryset().filter(edad__lt=18)
    
    @action(detail=False, methods=['get'])
    def estadisticas_menores(self, request):
        """
        Estadísticas específicas para menores retenidos
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Distribución por edad
        por_edad = queryset.values('edad').annotate(
            total=Count('id')
        ).order_by('edad')
        
        # Edad promedio
        edad_promedio = queryset.aggregate(Avg('edad'))['edad__avg']
        
        # Estadísticas por motivo de detención
        por_motivo = queryset.values(
            'motivo_detencion'
        ).annotate(
            total=Count('id')
        )
        
        # Menores en organizaciones criminales
        total_bbcc_oocc = queryset.filter(
            es_integrante_bbcc_oocc='SÍ'
        ).count()
        
        return Response({
            'total_menores': queryset.count(),
            'edad_promedio': round(edad_promedio, 1) if edad_promedio else None,
            'distribucion_por_edad': list(por_edad),
            'por_motivo_detencion': list(por_motivo),
            'total_en_bbcc_oocc': total_bbcc_oocc,
            'porcentaje_en_bbcc_oocc': round(
                (total_bbcc_oocc / queryset.count() * 100), 1
            ) if queryset.count() > 0 else 0
        })
    
    @action(detail=False, methods=['get'])
    def reporte_menores_riesgo(self, request):
        """
        Reporte especial de menores en situación de riesgo
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Menores en organizaciones criminales
        en_organizaciones = queryset.filter(es_integrante_bbcc_oocc='SÍ')
        
        # Menores con armas
        con_armas = queryset.filter(
            categoria_arma__isnull=False
        ).exclude(categoria_arma__nombre='NINGUNA')
        
        # Menores reincidentes (mismo documento, múltiples registros)
        from django.db.models import Count
        reincidentes = queryset.values(
            'numero_documento'
        ).annotate(
            total_registros=Count('id')
        ).filter(total_registros__gt=1)
        
        return Response({
            'resumen_riesgo': {
                'total_menores': queryset.count(),
                'en_organizaciones_criminales': en_organizaciones.count(),
                'con_armas': con_armas.count(),
                'posibles_reincidentes': reincidentes.count()
            },
            'organizaciones_mas_frecuentes': list(
                en_organizaciones.values('nombre_bbcc_oocc').annotate(
                    total=Count('id')
                ).order_by('-total')[:5]
            ),
            'tipos_arma_mas_frecuentes': list(
                con_armas.values('categoria_arma__nombre').annotate(
                    total=Count('id')
                ).order_by('-total')[:5]
            )
        })
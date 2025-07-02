from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg, Q
from production.models import (
    PlantillaEnvPBC, PlantillaEnvCC, PlantillaEnvMarihuana,
    PlantillaKgPBC, PlantillaKgCC, PlantillaKgMarihuana,
    PlantillaKgLatexOpio, PlantillaKgDrogaSintetica
)
from production.serializers import (
    PlantillaEnvPBCSerializer, PlantillaEnvCCSerializer, PlantillaEnvMarihuanaSerializer,
    PlantillaKgPBCSerializer, PlantillaKgCCSerializer, PlantillaKgMarihuanaSerializer,
    PlantillaKgLatexOpioSerializer, PlantillaKgDrogaSinteticaSerializer,
    # Serializers para listados
    PlantillaEnvPBCListSerializer, PlantillaEnvCCListSerializer, PlantillaEnvMarihuanaListSerializer,
    PlantillaKgPBCListSerializer, PlantillaKgCCListSerializer, PlantillaKgMarihuanaListSerializer,
    PlantillaKgLatexOpioListSerializer, PlantillaKgDrogaSinteticaListSerializer
)
from .base_views import FormularioDrogasViewSet


# =============================================================================
# VIEWSETS PARA FORMULARIOS DE ENVOLTORIOS
# =============================================================================

class PlantillaEnvPBCViewSet(FormularioDrogasViewSet):
    """
    ViewSet para el formulario de Envoltorios de Pasta Básica de Cocaína
    """
    queryset = PlantillaEnvPBC.objects.select_related(
        'departamento', 'provincia', 'distrito',
        'direccion_policial', 'direccion_especializada', 'division_policial',
        'departamento_policial', 'unidad_policial'
    ).all()
    
    serializer_class = PlantillaEnvPBCSerializer
    list_serializer_class = PlantillaEnvPBCListSerializer
    
    # Campos específicos para envoltorios
    filterset_fields = FormularioDrogasViewSet.filterset_fields + ['cantidad_unidades']
    ordering_fields = FormularioDrogasViewSet.ordering_fields + ['cantidad_unidades']
    
    def get_serializer_class(self):
        """Usar serializer simplificado para listados"""
        if self.action == 'list':
            return self.list_serializer_class
        return self.serializer_class


class PlantillaEnvCCViewSet(FormularioDrogasViewSet):
    """
    ViewSet para el formulario de Envoltorios de Clorhidrato de Cocaína
    """
    queryset = PlantillaEnvCC.objects.select_related(
        'departamento', 'provincia', 'distrito',
        'direccion_policial', 'direccion_especializada', 'division_policial',
        'departamento_policial', 'unidad_policial'
    ).all()
    
    serializer_class = PlantillaEnvCCSerializer
    list_serializer_class = PlantillaEnvCCListSerializer
    
    filterset_fields = FormularioDrogasViewSet.filterset_fields + ['cantidad_unidades']
    ordering_fields = FormularioDrogasViewSet.ordering_fields + ['cantidad_unidades']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return self.serializer_class


class PlantillaKgDrogaSinteticaViewSet(FormularioDrogasViewSet):
    """
    ViewSet para el formulario de Kilogramos de Droga Sintética
    """
    queryset = PlantillaKgDrogaSintetica.objects.select_related(
        'departamento', 'provincia', 'distrito',
        'direccion_policial', 'direccion_especializada', 'division_policial',
        'departamento_policial', 'unidad_policial'
    ).all()
    
    serializer_class = PlantillaKgDrogaSinteticaSerializer
    list_serializer_class = PlantillaKgDrogaSinteticaListSerializer
    
    filterset_fields = FormularioDrogasViewSet.filterset_fields + ['cantidad_kilogramos']
    ordering_fields = FormularioDrogasViewSet.ordering_fields + ['cantidad_kilogramos']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return self.serializer_class


# =============================================================================
# ENDPOINT CONSOLIDADO PARA ESTADÍSTICAS DE DROGAS
# =============================================================================

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estadisticas_drogas_consolidadas(request):
    """
    Endpoint consolidado para obtener estadísticas de todas las drogas
    """
    # Obtener parámetros de filtro
    fecha_desde = request.query_params.get('fecha_desde')
    fecha_hasta = request.query_params.get('fecha_hasta')
    departamento_id = request.query_params.get('departamento_id')
    
    # Función auxiliar para aplicar filtros
    def aplicar_filtros(queryset):
        if fecha_desde and fecha_hasta:
            queryset = queryset.filter(fecha_incautacion__range=[fecha_desde, fecha_hasta])
        if departamento_id:
            queryset = queryset.filter(departamento_id=departamento_id)
        return queryset
    
    # Estadísticas de envoltorios
    env_pbc = aplicar_filtros(PlantillaEnvPBC.objects.all())
    env_cc = aplicar_filtros(PlantillaEnvCC.objects.all())
    env_marihuana = aplicar_filtros(PlantillaEnvMarihuana.objects.all())
    
    # Estadísticas de kilogramos
    kg_pbc = aplicar_filtros(PlantillaKgPBC.objects.all())
    kg_cc = aplicar_filtros(PlantillaKgCC.objects.all())
    kg_marihuana = aplicar_filtros(PlantillaKgMarihuana.objects.all())
    kg_latex_opio = aplicar_filtros(PlantillaKgLatexOpio.objects.all())
    kg_droga_sintetica = aplicar_filtros(PlantillaKgDrogaSintetica.objects.all())
    
    # Consolidar estadísticas de envoltorios
    estadisticas_envoltorios = {
        'pbc': {
            'total_operativos': env_pbc.count(),
            'total_envoltorios': env_pbc.aggregate(Sum('cantidad_unidades'))['cantidad_unidades__sum'] or 0,
            'promedio_por_operativo': env_pbc.aggregate(Avg('cantidad_unidades'))['cantidad_unidades__avg'] or 0
        },
        'cc': {
            'total_operativos': env_cc.count(),
            'total_envoltorios': env_cc.aggregate(Sum('cantidad_unidades'))['cantidad_unidades__sum'] or 0,
            'promedio_por_operativo': env_cc.aggregate(Avg('cantidad_unidades'))['cantidad_unidades__avg'] or 0
        },
        'marihuana': {
            'total_operativos': env_marihuana.count(),
            'total_envoltorios': env_marihuana.aggregate(Sum('cantidad_unidades'))['cantidad_unidades__sum'] or 0,
            'promedio_por_operativo': env_marihuana.aggregate(Avg('cantidad_unidades'))['cantidad_unidades__avg'] or 0
        }
    }
    
    # Consolidar estadísticas de kilogramos
    estadisticas_kilogramos = {
        'pbc': {
            'total_operativos': kg_pbc.count(),
            'total_kilogramos': float(kg_pbc.aggregate(Sum('cantidad_kilogramos'))['cantidad_kilogramos__sum'] or 0),
            'promedio_por_operativo': float(kg_pbc.aggregate(Avg('cantidad_kilogramos'))['cantidad_kilogramos__avg'] or 0)
        },
        'cc': {
            'total_operativos': kg_cc.count(),
            'total_kilogramos': float(kg_cc.aggregate(Sum('cantidad_kilogramos'))['cantidad_kilogramos__sum'] or 0),
            'promedio_por_operativo': float(kg_cc.aggregate(Avg('cantidad_kilogramos'))['cantidad_kilogramos__avg'] or 0)
        },
        'marihuana': {
            'total_operativos': kg_marihuana.count(),
            'total_kilogramos': float(kg_marihuana.aggregate(Sum('cantidad_kilogramos'))['cantidad_kilogramos__sum'] or 0),
            'promedio_por_operativo': float(kg_marihuana.aggregate(Avg('cantidad_kilogramos'))['cantidad_kilogramos__avg'] or 0)
        },
        'latex_opio': {
            'total_operativos': kg_latex_opio.count(),
            'total_kilogramos': float(kg_latex_opio.aggregate(Sum('cantidad_kilogramos'))['cantidad_kilogramos__sum'] or 0),
            'promedio_por_operativo': float(kg_latex_opio.aggregate(Avg('cantidad_kilogramos'))['cantidad_kilogramos__avg'] or 0)
        },
        'droga_sintetica': {
            'total_operativos': kg_droga_sintetica.count(),
            'total_kilogramos': float(kg_droga_sintetica.aggregate(Sum('cantidad_kilogramos'))['cantidad_kilogramos__sum'] or 0),
            'promedio_por_operativo': float(kg_droga_sintetica.aggregate(Avg('cantidad_kilogramos'))['cantidad_kilogramos__avg'] or 0)
        }
    }
    
    # Estadísticas por ubicación (top 10 departamentos)
    from django.db.models import Case, When, Value, CharField
    
    # Unir todos los querysets con un identificador de tipo
    all_queries = []
    
    for modelo, tipo in [
        (PlantillaEnvPBC, 'ENV_PBC'), (PlantillaEnvCC, 'ENV_CC'), (PlantillaEnvMarihuana, 'ENV_MARIHUANA'),
        (PlantillaKgPBC, 'KG_PBC'), (PlantillaKgCC, 'KG_CC'), (PlantillaKgMarihuana, 'KG_MARIHUANA'),
        (PlantillaKgLatexOpio, 'KG_LATEX_OPIO'), (PlantillaKgDrogaSintetica, 'KG_DROGA_SINTETICA')
    ]:
        query = aplicar_filtros(modelo.objects.all()).values(
            'departamento__nombre'
        ).annotate(
            total=Count('id'),
            tipo_droga=Value(tipo, output_field=CharField())
        )
        all_queries.append(query)
    
    # Estadísticas por tipo de intervención
    operativo_count = 0
    intervencion_count = 0
    
    for modelo in [PlantillaEnvPBC, PlantillaEnvCC, PlantillaEnvMarihuana, 
                   PlantillaKgPBC, PlantillaKgCC, PlantillaKgMarihuana, 
                   PlantillaKgLatexOpio, PlantillaKgDrogaSintetica]:
        filtered_qs = aplicar_filtros(modelo.objects.all())
        operativo_count += filtered_qs.filter(tipo_intervencion='OPERATIVO').count()
        intervencion_count += filtered_qs.filter(tipo_intervencion='INTERVENCIÓN').count()
    
    return Response({
        'resumen_general': {
            'total_operativos_drogas': sum([
                env_pbc.count(), env_cc.count(), env_marihuana.count(),
                kg_pbc.count(), kg_cc.count(), kg_marihuana.count(),
                kg_latex_opio.count(), kg_droga_sintetica.count()
            ]),
            'por_tipo_intervencion': {
                'operativo': operativo_count,
                'intervencion': intervencion_count
            }
        },
        'envoltorios': estadisticas_envoltorios,
        'kilogramos': estadisticas_kilogramos,
        'filtros_aplicados': {
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'departamento_id': departamento_id
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ranking_incautaciones(request):
    """
    Endpoint para obtener ranking de incautaciones por diferentes criterios
    """
    tipo_ranking = request.query_params.get('tipo', 'departamento')  # departamento, unidad, mes
    limite = int(request.query_params.get('limite', 10))
    
    if tipo_ranking == 'departamento':
        # Ranking por departamento
        from django.db.models import Q
        
        # Combinar todos los modelos de drogas
        departamentos_stats = {}
        
        for modelo in [PlantillaEnvPBC, PlantillaEnvCC, PlantillaEnvMarihuana, 
                       PlantillaKgPBC, PlantillaKgCC, PlantillaKgMarihuana, 
                       PlantillaKgLatexOpio, PlantillaKgDrogaSintetica]:
            
            stats = modelo.objects.values(
                'departamento__nombre'
            ).annotate(
                total_operativos=Count('id')
            )
            
            for stat in stats:
                dep_nombre = stat['departamento__nombre']
                if dep_nombre not in departamentos_stats:
                    departamentos_stats[dep_nombre] = 0
                departamentos_stats[dep_nombre] += stat['total_operativos']
        
        # Convertir a lista y ordenar
        ranking = [
            {'departamento': nombre, 'total_operativos': total}
            for nombre, total in departamentos_stats.items()
        ]
        ranking.sort(key=lambda x: x['total_operativos'], reverse=True)
        
        return Response({
            'tipo_ranking': 'departamento',
            'top_departamentos': ranking[:limite]
        })
    
    elif tipo_ranking == 'unidad':
        # Ranking por unidad policial
        unidades_stats = {}
        
        for modelo in [PlantillaEnvPBC, PlantillaEnvCC, PlantillaEnvMarihuana, 
                       PlantillaKgPBC, PlantillaKgCC, PlantillaKgMarihuana, 
                       PlantillaKgLatexOpio, PlantillaKgDrogaSintetica]:
            
            stats = modelo.objects.filter(
                direccion_policial__isnull=False
            ).values(
                'direccion_policial__sigla',
                'direccion_policial__nombre'
            ).annotate(
                total_operativos=Count('id')
            )
            
            for stat in stats:
                sigla = stat['direccion_policial__sigla'] or stat['direccion_policial__nombre']
                if sigla not in unidades_stats:
                    unidades_stats[sigla] = {
                        'sigla': sigla,
                        'nombre': stat['direccion_policial__nombre'],
                        'total_operativos': 0
                    }
                unidades_stats[sigla]['total_operativos'] += stat['total_operativos']
        
        # Convertir a lista y ordenar
        ranking = list(unidades_stats.values())
        ranking.sort(key=lambda x: x['total_operativos'], reverse=True)
        
        return Response({
            'tipo_ranking': 'unidad_policial',
            'top_unidades': ranking[:limite]
        })
    
    else:
        return Response({
            'error': 'Tipo de ranking no válido. Opciones: departamento, unidad'
        }, status=status.HTTP_400_BAD_REQUEST).list_serializer_class
        return self.serializer_class


class PlantillaEnvMarihuanaViewSet(FormularioDrogasViewSet):
    """
    ViewSet para el formulario de Envoltorios de Marihuana
    """
    queryset = PlantillaEnvMarihuana.objects.select_related(
        'departamento', 'provincia', 'distrito',
        'direccion_policial', 'direccion_especializada', 'division_policial',
        'departamento_policial', 'unidad_policial'
    ).all()
    
    serializer_class = PlantillaEnvMarihuanaSerializer
    list_serializer_class = PlantillaEnvMarihuanaListSerializer
    
    filterset_fields = FormularioDrogasViewSet.filterset_fields + ['cantidad_unidades']
    ordering_fields = FormularioDrogasViewSet.ordering_fields + ['cantidad_unidades']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return self.serializer_class


# =============================================================================
# VIEWSETS PARA FORMULARIOS DE KILOGRAMOS
# =============================================================================

class PlantillaKgPBCViewSet(FormularioDrogasViewSet):
    """
    ViewSet para el formulario de Kilogramos de Pasta Básica de Cocaína
    """
    queryset = PlantillaKgPBC.objects.select_related(
        'departamento', 'provincia', 'distrito',
        'direccion_policial', 'direccion_especializada', 'division_policial',
        'departamento_policial', 'unidad_policial'
    ).all()
    
    serializer_class = PlantillaKgPBCSerializer
    list_serializer_class = PlantillaKgPBCListSerializer
    
    filterset_fields = FormularioDrogasViewSet.filterset_fields + ['cantidad_kilogramos']
    ordering_fields = FormularioDrogasViewSet.ordering_fields + ['cantidad_kilogramos']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return self.serializer_class


class PlantillaKgCCViewSet(FormularioDrogasViewSet):
    """
    ViewSet para el formulario de Kilogramos de Clorhidrato de Cocaína
    """
    queryset = PlantillaKgCC.objects.select_related(
        'departamento', 'provincia', 'distrito',
        'direccion_policial', 'direccion_especializada', 'division_policial',
        'departamento_policial', 'unidad_policial'
    ).all()
    
    serializer_class = PlantillaKgCCSerializer
    list_serializer_class = PlantillaKgCCListSerializer
    
    filterset_fields = FormularioDrogasViewSet.filterset_fields + ['cantidad_kilogramos']
    ordering_fields = FormularioDrogasViewSet.ordering_fields + ['cantidad_kilogramos']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return self.serializer_class


class PlantillaKgMarihuanaViewSet(FormularioDrogasViewSet):
    """
    ViewSet para el formulario de Kilogramos de Marihuana
    """
    queryset = PlantillaKgMarihuana.objects.select_related(
        'departamento', 'provincia', 'distrito',
        'direccion_policial', 'direccion_especializada', 'division_policial',
        'departamento_policial', 'unidad_policial'
    ).all()
    
    serializer_class = PlantillaKgMarihuanaSerializer
    list_serializer_class = PlantillaKgMarihuanaListSerializer
    
    filterset_fields = FormularioDrogasViewSet.filterset_fields + ['cantidad_kilogramos']
    ordering_fields = FormularioDrogasViewSet.ordering_fields + ['cantidad_kilogramos']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return self.serializer_class


class PlantillaKgLatexOpioViewSet(FormularioDrogasViewSet):
    """
    ViewSet para el formulario de Kilogramos de Látex de Opio
    """
    queryset = PlantillaKgLatexOpio.objects.select_related(
        'departamento', 'provincia', 'distrito',
        'direccion_policial', 'direccion_especializada', 'division_policial',
        'departamento_policial', 'unidad_policial'
    ).all()
    
    serializer_class = PlantillaKgLatexOpioSerializer
    list_serializer_class = PlantillaKgLatexOpioListSerializer
    
    filterset_fields = FormularioDrogasViewSet.filterset_fields + ['cantidad_kilogramos']
    ordering_fields = FormularioDrogasViewSet.ordering_fields + ['cantidad_kilogramos']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return self
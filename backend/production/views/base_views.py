from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

User = get_user_model()


# =============================================================================
# VIEWSETS BASE Y MIXINS REUTILIZABLES
# =============================================================================

class BaseFormularioViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para todos los formularios con funcionalidades comunes
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """
        Personalizar creación de registros:
        - Asignar usuario creador
        - Auto-generar número de registro
        """
        # Obtener el último número de registro para este tipo de formulario
        model_class = serializer.Meta.model
        last_record = model_class.objects.order_by('-numero_registro').first()
        next_number = (last_record.numero_registro + 1) if last_record else 1
        
        # Guardar con metadatos
        serializer.save(
            created_by=self.request.user,
            numero_registro=next_number
        )
    
    def perform_update(self, serializer):
        """
        Personalizar actualización de registros:
        - Asignar usuario que actualiza
        """
        serializer.save(updated_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Endpoint para obtener estadísticas básicas del formulario
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Estadísticas básicas
        total_registros = queryset.count()
        
        # Estadísticas por fecha (último mes)
        from datetime import datetime, timedelta
        fecha_limite = timezone.now() - timedelta(days=30)
        
        # Determinar campo de fecha según el tipo de formulario
        fecha_field = 'fecha_detencion' if hasattr(queryset.model, 'fecha_detencion') else 'fecha_incautacion'
        
        registros_ultimo_mes = queryset.filter(
            **{f'{fecha_field}__gte': fecha_limite.date()}
        ).count()
        
        # Estadísticas por ubicación (si tiene)
        estadisticas_ubicacion = []
        if hasattr(queryset.model, 'departamento'):
            from django.db.models import Count
            ubicacion_stats = queryset.values('departamento__nombre').annotate(
                total=Count('id')
            ).order_by('-total')[:10]
            estadisticas_ubicacion = list(ubicacion_stats)
        
        return Response({
            'total_registros': total_registros,
            'registros_ultimo_mes': registros_ultimo_mes,
            'estadisticas_ubicacion': estadisticas_ubicacion,
            'fecha_consulta': timezone.now()
        })
    
    @action(detail=False, methods=['get'])
    def exportar_excel(self, request):
        """
        Endpoint para exportar datos a Excel
        """
        # Aquí se implementaría la lógica de exportación
        # Por ahora retornamos la información de los registros filtrados
        queryset = self.filter_queryset(self.get_queryset())
        
        return Response({
            'message': 'Funcionalidad de exportación disponible',
            'total_registros': queryset.count(),
            'formato': 'excel'
        })


class BaseReferenceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet base para tablas de referencia (solo lectura)
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre']
    ordering = ['nombre']


# =============================================================================
# MIXINS PARA FUNCIONALIDADES ESPECÍFICAS
# =============================================================================

class FiltrosCascadaMixin:
    """
    Mixin para endpoints con filtros cascada (ubicación, delitos, etc.)
    """
    
    @action(detail=False, methods=['get'])
    def opciones_cascada(self, request):
        """
        Endpoint genérico para obtener opciones de filtros cascada
        """
        tipo_filtro = request.query_params.get('tipo')
        padre_id = request.query_params.get('padre_id')
        
        if not tipo_filtro:
            return Response({
                'error': 'Se requiere el parámetro "tipo"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Implementar lógica específica según el tipo
        return Response({
            'tipo': tipo_filtro,
            'padre_id': padre_id,
            'opciones': []
        })


class BusquedaAvanzadaMixin:
    """
    Mixin para búsquedas avanzadas en formularios
    """
    
    @action(detail=False, methods=['get'])
    def busqueda_avanzada(self, request):
        """
        Endpoint para búsquedas avanzadas con múltiples criterios
        """
        queryset = self.get_queryset()
        
        # Filtros por fecha
        fecha_desde = request.query_params.get('fecha_desde')
        fecha_hasta = request.query_params.get('fecha_hasta')
        
        if fecha_desde and fecha_hasta:
            # Determinar campo de fecha según el modelo
            fecha_field = 'fecha_detencion' if hasattr(queryset.model, 'fecha_detencion') else 'fecha_incautacion'
            queryset = queryset.filter(
                **{f'{fecha_field}__range': [fecha_desde, fecha_hasta]}
            )
        
        # Filtro por ubicación
        departamento_id = request.query_params.get('departamento_id')
        if departamento_id and hasattr(queryset.model, 'departamento'):
            queryset = queryset.filter(departamento_id=departamento_id)
        
        provincia_id = request.query_params.get('provincia_id')
        if provincia_id and hasattr(queryset.model, 'provincia'):
            queryset = queryset.filter(provincia_id=provincia_id)
        
        distrito_id = request.query_params.get('distrito_id')
        if distrito_id and hasattr(queryset.model, 'distrito'):
            queryset = queryset.filter(distrito_id=distrito_id)
        
        # Filtro por unidad policial
        direccion_policial_id = request.query_params.get('direccion_policial_id')
        if direccion_policial_id and hasattr(queryset.model, 'direccion_policial'):
            queryset = queryset.filter(direccion_policial_id=direccion_policial_id)
        
        # Filtro de texto libre
        texto_libre = request.query_params.get('texto_libre')
        if texto_libre:
            # Buscar en varios campos según el tipo de formulario
            q_objects = Q()
            
            # Campos comunes de persona
            if hasattr(queryset.model, 'apellido_paterno'):
                q_objects |= Q(apellido_paterno__icontains=texto_libre)
                q_objects |= Q(apellido_materno__icontains=texto_libre)
                q_objects |= Q(nombres__icontains=texto_libre)
                q_objects |= Q(numero_documento__icontains=texto_libre)
            
            # Campo de notas
            if hasattr(queryset.model, 'nota_informativa_sicpip'):
                q_objects |= Q(nota_informativa_sicpip__icontains=texto_libre)
            
            queryset = queryset.filter(q_objects)
        
        # Aplicar paginación y serialización
        page = self.paginate_queryset(queryset)
        if page is not None:
            # Usar serializer simplificado para listados si está disponible
            list_serializer_class = getattr(self, 'list_serializer_class', None)
            if list_serializer_class:
                serializer = list_serializer_class(page, many=True, context={'request': request})
            else:
                serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        # Si no hay paginación
        list_serializer_class = getattr(self, 'list_serializer_class', None)
        if list_serializer_class:
            serializer = list_serializer_class(queryset, many=True, context={'request': request})
        else:
            serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data)


class ReportesMixin:
    """
    Mixin para generar reportes y estadísticas
    """
    
    @action(detail=False, methods=['get'])
    def reporte_resumen(self, request):
        """
        Endpoint para obtener resumen estadístico
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Estadísticas básicas
        total = queryset.count()
        
        # Agrupar por fecha (últimos 30 días)
        from datetime import datetime, timedelta
        from django.db.models import Count, F
        
        fecha_limite = timezone.now() - timedelta(days=30)
        fecha_field = 'fecha_detencion' if hasattr(queryset.model, 'fecha_detencion') else 'fecha_incautacion'
        
        registros_por_fecha = queryset.filter(
            **{f'{fecha_field}__gte': fecha_limite.date()}
        ).extra(
            select={'fecha': f'date({fecha_field})'}
        ).values('fecha').annotate(
            total=Count('id')
        ).order_by('fecha')
        
        # Agrupar por ubicación
        por_departamento = []
        if hasattr(queryset.model, 'departamento'):
            por_departamento = queryset.values(
                'departamento__nombre'
            ).annotate(
                total=Count('id')
            ).order_by('-total')[:10]
        
        # Agrupar por unidad policial
        por_unidad = []
        if hasattr(queryset.model, 'direccion_policial'):
            por_unidad = queryset.values(
                'direccion_policial__sigla',
                'direccion_policial__nombre'
            ).annotate(
                total=Count('id')
            ).order_by('-total')[:10]
        
        return Response({
            'resumen': {
                'total_registros': total,
                'periodo_analisis': '30 días',
                'fecha_generacion': timezone.now()
            },
            'por_fecha': list(registros_por_fecha),
            'por_departamento': list(por_departamento),
            'por_unidad_policial': list(por_unidad)
        })


# =============================================================================
# VIEWSETS ESPECÍFICOS POR TIPO
# =============================================================================

class FormularioPersonasViewSet(BaseFormularioViewSet, BusquedaAvanzadaMixin, ReportesMixin):
    """
    ViewSet especializado para formularios de personas
    """
    search_fields = [
        'apellido_paterno', 'apellido_materno', 'nombres', 
        'numero_documento', 'nota_informativa_sicpip'
    ]
    filterset_fields = [
        'genero', 'edad', 'nacionalidad', 'tipo_documento',
        'departamento', 'provincia', 'distrito',
        'es_funcionario_publico', 'direccion_policial'
    ]
    ordering_fields = [
        'numero_registro', 'fecha_detencion', 'apellido_paterno', 
        'apellido_materno', 'nombres', 'edad'
    ]
    
    @action(detail=False, methods=['get'])
    def estadisticas_personas(self, request):
        """
        Estadísticas específicas para formularios de personas
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        from django.db.models import Count, Avg
        
        # Estadísticas por género
        por_genero = queryset.values('genero').annotate(
            total=Count('id')
        ).order_by('genero')
        
        # Estadísticas por edad
        edad_promedio = queryset.aggregate(Avg('edad'))['edad__avg']
        
        # Estadísticas por nacionalidad
        por_nacionalidad = queryset.values(
            'nacionalidad__nombre'
        ).annotate(
            total=Count('id')
        ).order_by('-total')[:10]
        
        return Response({
            'por_genero': list(por_genero),
            'edad_promedio': round(edad_promedio, 1) if edad_promedio else None,
            'por_nacionalidad': list(por_nacionalidad)
        })


class FormularioDrogasViewSet(BaseFormularioViewSet, BusquedaAvanzadaMixin, ReportesMixin):
    """
    ViewSet especializado para formularios de drogas
    """
    search_fields = ['nota_informativa_sicpip']
    filterset_fields = [
        'departamento', 'provincia', 'distrito',
        'direccion_policial', 'tipo_intervencion'
    ]
    ordering_fields = [
        'numero_registro', 'fecha_incautacion', 'cantidad_unidades', 'cantidad_kilogramos'
    ]
    
    @action(detail=False, methods=['get'])
    def estadisticas_drogas(self, request):
        """
        Estadísticas específicas para formularios de drogas
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        from django.db.models import Sum, Count, Avg
        
        # Totales según el tipo
        resultado = {
            'total_registros': queryset.count()
        }
        
        # Si el modelo tiene cantidad_unidades (envoltorios)
        if hasattr(queryset.model, 'cantidad_unidades'):
            total_unidades = queryset.aggregate(Sum('cantidad_unidades'))['cantidad_unidades__sum']
            promedio_unidades = queryset.aggregate(Avg('cantidad_unidades'))['cantidad_unidades__avg']
            
            resultado.update({
                'total_unidades_incautadas': total_unidades or 0,
                'promedio_unidades_por_operativo': round(promedio_unidades, 1) if promedio_unidades else 0
            })
        
        # Si el modelo tiene cantidad_kilogramos
        if hasattr(queryset.model, 'cantidad_kilogramos'):
            total_kilogramos = queryset.aggregate(Sum('cantidad_kilogramos'))['cantidad_kilogramos__sum']
            promedio_kilogramos = queryset.aggregate(Avg('cantidad_kilogramos'))['cantidad_kilogramos__avg']
            
            resultado.update({
                'total_kilogramos_incautados': float(total_kilogramos or 0),
                'promedio_kilogramos_por_operativo': round(float(promedio_kilogramos or 0), 3)
            })
        
        # Por tipo de intervención
        por_tipo_intervencion = queryset.values('tipo_intervencion').annotate(
            total=Count('id')
        ).order_by('-total')
        
        resultado['por_tipo_intervencion'] = list(por_tipo_intervencion)
        
        return Response(resultado)
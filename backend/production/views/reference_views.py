from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
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
from production.serializers import (
    # Ubicación
    DepartamentoSerializer, ProvinciaSerializer, DistritoSerializer,
    ProvinciasPorDepartamentoSerializer, DistritosPorProvinciaSerializer,
    # Personas
    NacionalidadSerializer, TipoDocumentoSerializer, TipoRequisitoriaSerializer,
    # Delitos
    DelitoFueroSerializer, DelitoGeneralSerializer, DelitoEspecificoSerializer, DelitoSubtipoSerializer,
    DelitosGeneralesPorFueroSerializer, DelitosEspecificosPorGeneralSerializer, DelitosSubtiposPorEspecificoSerializer,
    # Estructura Policial
    DireccionPolicialSerializer, DireccionEspecializadaSerializer, DivisionPolicialSerializer,
    DepartamentoPolicialSerializer, UnidadPolicialSerializer,
    DireccionesEspecializadasPorDireccionSerializer,
    # Armas
    CategoriaArmaSerializer, TipoArmaSerializer, TiposArmaPorCategoriaSerializer,
    # Judicial
    SituacionDetenidoSerializer, FiscaliaSerializer
)
from .base_views import BaseReferenceViewSet, FiltrosCascadaMixin


# =============================================================================
# VIEWSETS DE UBICACIÓN GEOGRÁFICA
# =============================================================================

class DepartamentoViewSet(BaseReferenceViewSet):
    """
    ViewSet para Departamentos
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    search_fields = ['nombre', 'codigo']
    ordering_fields = ['nombre', 'codigo']


class ProvinciaViewSet(BaseReferenceViewSet, FiltrosCascadaMixin):
    """
    ViewSet para Provincias con filtros por departamento
    """
    queryset = Provincia.objects.select_related('departamento').all()
    serializer_class = ProvinciaSerializer
    search_fields = ['nombre', 'codigo', 'departamento__nombre']
    filterset_fields = ['departamento']
    ordering_fields = ['nombre', 'codigo', 'departamento__nombre']
    
    @action(detail=False, methods=['get'])
    def por_departamento(self, request):
        """
        Obtener provincias filtradas por departamento
        """
        departamento_id = request.query_params.get('departamento_id')
        
        if not departamento_id:
            return Response({
                'error': 'Se requiere el parámetro departamento_id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        provincias = Provincia.objects.filter(
            departamento_id=departamento_id
        ).order_by('nombre')
        
        serializer = ProvinciasPorDepartamentoSerializer(provincias, many=True)
        return Response(serializer.data)


class DistritoViewSet(BaseReferenceViewSet, FiltrosCascadaMixin):
    """
    ViewSet para Distritos con filtros por provincia
    """
    queryset = Distrito.objects.select_related('provincia', 'provincia__departamento').all()
    serializer_class = DistritoSerializer
    search_fields = ['nombre', 'codigo', 'provincia__nombre', 'provincia__departamento__nombre']
    filterset_fields = ['provincia', 'provincia__departamento']
    ordering_fields = ['nombre', 'codigo']
    
    @action(detail=False, methods=['get'])
    def por_provincia(self, request):
        """
        Obtener distritos filtrados por provincia
        """
        provincia_id = request.query_params.get('provincia_id')
        
        if not provincia_id:
            return Response({
                'error': 'Se requiere el parámetro provincia_id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        distritos = Distrito.objects.filter(
            provincia_id=provincia_id
        ).order_by('nombre')
        
        serializer = DistritosPorProvinciaSerializer(distritos, many=True)
        return Response(serializer.data)


# =============================================================================
# VIEWSETS DE DATOS DE PERSONAS
# =============================================================================

class NacionalidadViewSet(BaseReferenceViewSet):
    """
    ViewSet para Nacionalidades
    """
    queryset = Nacionalidad.objects.all()
    serializer_class = NacionalidadSerializer
    search_fields = ['nombre', 'codigo']
    ordering_fields = ['nombre', 'codigo']


class TipoDocumentoViewSet(BaseReferenceViewSet):
    """
    ViewSet para Tipos de Documento
    """
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer
    search_fields = ['nombre', 'codigo']
    ordering_fields = ['nombre', 'codigo']


class TipoRequisitoriaViewSet(BaseReferenceViewSet):
    """
    ViewSet para Tipos de Requisitoria
    """
    queryset = TipoRequisitoria.objects.all()
    serializer_class = TipoRequisitoriaSerializer
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre']


# =============================================================================
# VIEWSETS DE DELITOS
# =============================================================================

class DelitoFueroViewSet(BaseReferenceViewSet):
    """
    ViewSet para Delitos Fuero
    """
    queryset = DelitoFuero.objects.all()
    serializer_class = DelitoFueroSerializer
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre']


class DelitoGeneralViewSet(BaseReferenceViewSet, FiltrosCascadaMixin):
    """
    ViewSet para Delitos Generales con filtros por fuero
    """
    queryset = DelitoGeneral.objects.select_related('delito_fuero').all()
    serializer_class = DelitoGeneralSerializer
    search_fields = ['nombre', 'descripcion', 'delito_fuero__nombre']
    filterset_fields = ['delito_fuero']
    ordering_fields = ['nombre', 'delito_fuero__nombre']
    
    @action(detail=False, methods=['get'])
    def por_fuero(self, request):
        """
        Obtener delitos generales filtrados por fuero
        """
        fuero_id = request.query_params.get('fuero_id')
        
        if not fuero_id:
            return Response({
                'error': 'Se requiere el parámetro fuero_id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        delitos = DelitoGeneral.objects.filter(
            delito_fuero_id=fuero_id
        ).order_by('nombre')
        
        serializer = DelitosGeneralesPorFueroSerializer(delitos, many=True)
        return Response(serializer.data)


class DelitoEspecificoViewSet(BaseReferenceViewSet, FiltrosCascadaMixin):
    """
    ViewSet para Delitos Específicos con filtros por general
    """
    queryset = DelitoEspecifico.objects.select_related(
        'delito_general', 'delito_general__delito_fuero'
    ).all()
    serializer_class = DelitoEspecificoSerializer
    search_fields = ['nombre', 'descripcion', 'delito_general__nombre']
    filterset_fields = ['delito_general', 'delito_general__delito_fuero']
    ordering_fields = ['nombre', 'delito_general__nombre']
    
    @action(detail=False, methods=['get'])
    def por_general(self, request):
        """
        Obtener delitos específicos filtrados por delito general
        """
        general_id = request.query_params.get('general_id')
        
        if not general_id:
            return Response({
                'error': 'Se requiere el parámetro general_id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        delitos = DelitoEspecifico.objects.filter(
            delito_general_id=general_id
        ).order_by('nombre')
        
        serializer = DelitosEspecificosPorGeneralSerializer(delitos, many=True)
        return Response(serializer.data)


class DelitoSubtipoViewSet(BaseReferenceViewSet, FiltrosCascadaMixin):
    """
    ViewSet para Delitos Subtipos con filtros por específico
    """
    queryset = DelitoSubtipo.objects.select_related(
        'delito_especifico', 'delito_especifico__delito_general', 
        'delito_especifico__delito_general__delito_fuero'
    ).all()
    serializer_class = DelitoSubtipoSerializer
    search_fields = ['nombre', 'descripcion', 'delito_especifico__nombre']
    filterset_fields = ['delito_especifico', 'delito_especifico__delito_general']
    ordering_fields = ['nombre', 'delito_especifico__nombre']
    
    @action(detail=False, methods=['get'])
    def por_especifico(self, request):
        """
        Obtener delitos subtipos filtrados por delito específico
        """
        especifico_id = request.query_params.get('especifico_id')
        
        if not especifico_id:
            return Response({
                'error': 'Se requiere el parámetro especifico_id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        subtipos = DelitoSubtipo.objects.filter(
            delito_especifico_id=especifico_id
        ).order_by('nombre')
        
        serializer = DelitosSubtiposPorEspecificoSerializer(subtipos, many=True)
        return Response(serializer.data)


# =============================================================================
# VIEWSETS DE ESTRUCTURA POLICIAL
# =============================================================================

class DireccionPolicialViewSet(BaseReferenceViewSet):
    """
    ViewSet para Direcciones Policiales
    """
    queryset = DireccionPolicial.objects.all()
    serializer_class = DireccionPolicialSerializer
    search_fields = ['nombre', 'sigla', 'descripcion']
    ordering_fields = ['nombre', 'sigla']


class DireccionEspecializadaViewSet(BaseReferenceViewSet, FiltrosCascadaMixin):
    """
    ViewSet para Direcciones Especializadas con filtros por dirección policial
    """
    queryset = DireccionEspecializada.objects.select_related('direccion_policial').all()
    serializer_class = DireccionEspecializadaSerializer
    search_fields = ['nombre', 'sigla', 'descripcion', 'direccion_policial__nombre']
    filterset_fields = ['direccion_policial']
    ordering_fields = ['nombre', 'sigla', 'direccion_policial__nombre']
    
    @action(detail=False, methods=['get'])
    def por_direccion(self, request):
        """
        Obtener direcciones especializadas filtradas por dirección policial
        """
        direccion_id = request.query_params.get('direccion_id')
        
        if not direccion_id:
            return Response({
                'error': 'Se requiere el parámetro direccion_id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        especializadas = DireccionEspecializada.objects.filter(
            direccion_policial_id=direccion_id
        ).order_by('nombre')
        
        serializer = DireccionesEspecializadasPorDireccionSerializer(especializadas, many=True)
        return Response(serializer.data)


class DivisionPolicialViewSet(BaseReferenceViewSet):
    """
    ViewSet para Divisiones Policiales
    """
    queryset = DivisionPolicial.objects.all()
    serializer_class = DivisionPolicialSerializer
    search_fields = ['nombre', 'sigla', 'descripcion']
    ordering_fields = ['nombre', 'sigla']


class DepartamentoPolicialViewSet(BaseReferenceViewSet):
    """
    ViewSet para Departamentos Policiales
    """
    queryset = DepartamentoPolicial.objects.all()
    serializer_class = DepartamentoPolicialSerializer
    search_fields = ['nombre', 'sigla', 'descripcion']
    ordering_fields = ['nombre', 'sigla']


class UnidadPolicialViewSet(BaseReferenceViewSet):
    """
    ViewSet para Unidades Policiales
    """
    queryset = UnidadPolicial.objects.all()
    serializer_class = UnidadPolicialSerializer
    search_fields = ['nombre', 'sigla', 'descripcion']
    ordering_fields = ['nombre', 'sigla']


# =============================================================================
# VIEWSETS DE ARMAS
# =============================================================================

class CategoriaArmaViewSet(BaseReferenceViewSet):
    """
    ViewSet para Categorías de Armas
    """
    queryset = CategoriaArma.objects.all()
    serializer_class = CategoriaArmaSerializer
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre']


class TipoArmaViewSet(BaseReferenceViewSet, FiltrosCascadaMixin):
    """
    ViewSet para Tipos de Armas con filtros por categoría
    """
    queryset = TipoArma.objects.select_related('categoria_arma').all()
    serializer_class = TipoArmaSerializer
    search_fields = ['nombre', 'descripcion', 'categoria_arma__nombre']
    filterset_fields = ['categoria_arma']
    ordering_fields = ['nombre', 'categoria_arma__nombre']
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """
        Obtener tipos de arma filtrados por categoría
        """
        categoria_id = request.query_params.get('categoria_id')
        
        if not categoria_id:
            return Response({
                'error': 'Se requiere el parámetro categoria_id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        tipos = TipoArma.objects.filter(
            categoria_arma_id=categoria_id
        ).order_by('nombre')
        
        serializer = TiposArmaPorCategoriaSerializer(tipos, many=True)
        return Response(serializer.data)


# =============================================================================
# VIEWSETS JUDICIALES
# =============================================================================

class SituacionDetenidoViewSet(BaseReferenceViewSet):
    """
    ViewSet para Situaciones del Detenido
    """
    queryset = SituacionDetenido.objects.all()
    serializer_class = SituacionDetenidoSerializer
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre']


class FiscaliaViewSet(BaseReferenceViewSet):
    """
    ViewSet para Fiscalías
    """
    queryset = Fiscalia.objects.select_related('departamento').all()
    serializer_class = FiscaliaSerializer
    search_fields = ['nombre', 'direccion', 'departamento__nombre']
    filterset_fields = ['departamento']
    ordering_fields = ['nombre', 'departamento__nombre']


# =============================================================================
# ENDPOINT GLOBAL PARA FILTROS CASCADA
# =============================================================================

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filtros_cascada_global(request):
    """
    Endpoint unificado para todos los filtros cascada del sistema
    """
    tipo = request.query_params.get('tipo')
    padre_id = request.query_params.get('padre_id')
    
    if not tipo:
        return Response({
            'error': 'Se requiere el parámetro "tipo"',
            'tipos_disponibles': [
                'provincias_por_departamento',
                'distritos_por_provincia', 
                'delitos_generales_por_fuero',
                'delitos_especificos_por_general',
                'delitos_subtipos_por_especifico',
                'direcciones_especializadas_por_direccion',
                'tipos_arma_por_categoria'
            ]
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        if tipo == 'provincias_por_departamento':
            if not padre_id:
                return Response({'error': 'Se requiere departamento_id'}, status=status.HTTP_400_BAD_REQUEST)
            
            provincias = Provincia.objects.filter(departamento_id=padre_id).order_by('nombre')
            serializer = ProvinciasPorDepartamentoSerializer(provincias, many=True)
            return Response(serializer.data)
        
        elif tipo == 'distritos_por_provincia':
            if not padre_id:
                return Response({'error': 'Se requiere provincia_id'}, status=status.HTTP_400_BAD_REQUEST)
            
            distritos = Distrito.objects.filter(provincia_id=padre_id).order_by('nombre')
            serializer = DistritosPorProvinciaSerializer(distritos, many=True)
            return Response(serializer.data)
        
        elif tipo == 'delitos_generales_por_fuero':
            if not padre_id:
                return Response({'error': 'Se requiere fuero_id'}, status=status.HTTP_400_BAD_REQUEST)
            
            delitos = DelitoGeneral.objects.filter(delito_fuero_id=padre_id).order_by('nombre')
            serializer = DelitosGeneralesPorFueroSerializer(delitos, many=True)
            return Response(serializer.data)
        
        elif tipo == 'delitos_especificos_por_general':
            if not padre_id:
                return Response({'error': 'Se requiere general_id'}, status=status.HTTP_400_BAD_REQUEST)
            
            delitos = DelitoEspecifico.objects.filter(delito_general_id=padre_id).order_by('nombre')
            serializer = DelitosEspecificosPorGeneralSerializer(delitos, many=True)
            return Response(serializer.data)
        
        elif tipo == 'delitos_subtipos_por_especifico':
            if not padre_id:
                return Response({'error': 'Se requiere especifico_id'}, status=status.HTTP_400_BAD_REQUEST)
            
            subtipos = DelitoSubtipo.objects.filter(delito_especifico_id=padre_id).order_by('nombre')
            serializer = DelitosSubtiposPorEspecificoSerializer(subtipos, many=True)
            return Response(serializer.data)
        
        elif tipo == 'direcciones_especializadas_por_direccion':
            if not padre_id:
                return Response({'error': 'Se requiere direccion_id'}, status=status.HTTP_400_BAD_REQUEST)
            
            especializadas = DireccionEspecializada.objects.filter(direccion_policial_id=padre_id).order_by('nombre')
            serializer = DireccionesEspecializadasPorDireccionSerializer(especializadas, many=True)
            return Response(serializer.data)
        
        elif tipo == 'tipos_arma_por_categoria':
            if not padre_id:
                return Response({'error': 'Se requiere categoria_id'}, status=status.HTTP_400_BAD_REQUEST)
            
            tipos = TipoArma.objects.filter(categoria_arma_id=padre_id).order_by('nombre')
            serializer = TiposArmaPorCategoriaSerializer(tipos, many=True)
            return Response(serializer.data)
        
        else:
            return Response({
                'error': f'Tipo "{tipo}" no reconocido'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'error': f'Error procesando filtro: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
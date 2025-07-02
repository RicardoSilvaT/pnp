import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  PlusIcon, 
  MagnifyingGlassIcon,
  PencilIcon,
  EyeIcon,
  TrashIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline';
import { rqAPI } from '../services/productionAPI';

const RQPage = () => {
  // Estados
  const [rqList, setRqList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);

  // Cargar datos al montar el componente
  useEffect(() => {
    loadRQData();
  }, [currentPage, searchTerm]);

  // Función para cargar datos
  const loadRQData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const params = {
        page: currentPage,
        page_size: 20,
      };
      
      if (searchTerm.trim()) {
        params.search = searchTerm.trim();
      }
      
      const response = await rqAPI.getAll(params);
      
      setRqList(response.results || []);
      setTotalRecords(response.count || 0);
      setTotalPages(Math.ceil((response.count || 0) / 20));
      
    } catch (err) {
      setError('Error al cargar los datos: ' + err.message);
      console.error('Error loading RQ data:', err);
    } finally {
      setLoading(false);
    }
  };

  // Función para eliminar registro
  const handleDelete = async (id, nombre) => {
    if (!window.confirm(`¿Está seguro de eliminar el registro de ${nombre}?`)) {
      return;
    }

    try {
      await rqAPI.delete(id);
      loadRQData(); // Recargar lista
      alert('Registro eliminado correctamente');
    } catch (err) {
      alert('Error al eliminar: ' + err.message);
    }
  };

  // Función para manejar búsqueda
  const handleSearch = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    loadRQData();
  };

  // Formatear fecha
  const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('es-PE');
  };

  // Formatear hora
  const formatTime = (timeString) => {
    if (!timeString) return '';
    return timeString.slice(0, 5); // HH:MM
  };

  return (
    <div className="space-y-6">
      {/* Encabezado */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-red-100 p-2 rounded-lg">
              <DocumentTextIcon className="h-6 w-6 text-red-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Requisitorias (RQ)</h1>
              <p className="text-gray-600">Personas detenidas por requisitorias</p>
            </div>
          </div>
          <Link
            to="/ofad/produccion/personas/rq/create"
            className="flex items-center space-x-2 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors"
          >
            <PlusIcon className="h-5 w-5" />
            <span>Nuevo RQ</span>
          </Link>
        </div>
      </div>

      {/* Barra de búsqueda y filtros */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <form onSubmit={handleSearch} className="flex items-center space-x-4">
          <div className="flex-1">
            <div className="relative">
              <MagnifyingGlassIcon className="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Buscar por nombre, apellido o número de documento..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-red-500 focus:border-transparent"
              />
            </div>
          </div>
          <button
            type="submit"
            className="bg-gray-600 text-white px-6 py-2 rounded-md hover:bg-gray-700 transition-colors"
          >
            Buscar
          </button>
          <button
            type="button"
            onClick={() => {
              setSearchTerm('');
              setCurrentPage(1);
              loadRQData();
            }}
            className="bg-gray-300 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-400 transition-colors"
          >
            Limpiar
          </button>
        </form>
      </div>

      {/* Contenido principal */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        {/* Estadísticas rápidas */}
        <div className="border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-600">
              Mostrando {rqList.length} de {totalRecords} registros
            </div>
            <div className="text-sm text-gray-600">
              Página {currentPage} de {totalPages}
            </div>
          </div>
        </div>

        {/* Estado de carga */}
        {loading && (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Cargando datos...</p>
          </div>
        )}

        {/* Estado de error */}
        {error && (
          <div className="p-6">
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <p className="text-red-800">{error}</p>
              <button
                onClick={loadRQData}
                className="mt-2 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors"
              >
                Reintentar
              </button>
            </div>
          </div>
        )}

        {/* Tabla de datos */}
        {!loading && !error && (
          <>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      N° Registro
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Fecha/Hora
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Persona
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Documento
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Tipo RQ
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Más Buscados
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Acciones
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {rqList.length === 0 ? (
                    <tr>
                      <td colSpan="7" className="px-6 py-8 text-center text-gray-500">
                        <DocumentTextIcon className="h-12 w-12 mx-auto text-gray-300 mb-4" />
                        <p>No se encontraron registros de RQ</p>
                        <Link
                          to="/ofad/produccion/personas/rq/create"
                          className="mt-2 inline-flex items-center text-red-600 hover:text-red-800"
                        >
                          <PlusIcon className="h-4 w-4 mr-1" />
                          Crear primer RQ
                        </Link>
                      </td>
                    </tr>
                  ) : (
                    rqList.map((rq) => (
                      <tr key={rq.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          RQ-{String(rq.numero_registro).padStart(3, '0')}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          <div>
                            <div>{formatDate(rq.fecha_detencion)}</div>
                            <div className="text-xs text-gray-500">{formatTime(rq.hora_detencion)}</div>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          <div>
                            <div className="font-medium">
                              {rq.apellido_paterno} {rq.apellido_materno}
                            </div>
                            <div className="text-gray-600">{rq.nombres}</div>
                            <div className="text-xs text-gray-500">
                              {rq.edad} años - {rq.genero}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          <div>
                            <div>{rq.numero_documento}</div>
                            <div className="text-xs text-gray-500">
                              {rq.tipo_documento_data?.nombre}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {rq.tipo_requisitoria_data?.nombre}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            rq.esta_en_lista_mas_buscados === 'SÍ'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-gray-100 text-gray-800'
                          }`}>
                            {rq.esta_en_lista_mas_buscados}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => {/* Ver detalles */}}
                              className="text-blue-600 hover:text-blue-800"
                              title="Ver detalles"
                            >
                              <EyeIcon className="h-4 w-4" />
                            </button>
                            <Link
                              to={`/ofad/produccion/personas/rq/edit/${rq.id}`}
                              className="text-green-600 hover:text-green-800"
                              title="Editar"
                            >
                              <PencilIcon className="h-4 w-4" />
                            </Link>
                            <button
                              onClick={() => handleDelete(rq.id, `${rq.nombres} ${rq.apellido_paterno}`)}
                              className="text-red-600 hover:text-red-800"
                              title="Eliminar"
                            >
                              <TrashIcon className="h-4 w-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

            {/* Paginación */}
            {totalPages > 1 && (
              <div className="border-t border-gray-200 px-6 py-4">
                <div className="flex items-center justify-between">
                  <button
                    onClick={() => setCurrentPage(currentPage - 1)}
                    disabled={currentPage === 1}
                    className={`px-4 py-2 text-sm font-medium rounded-md ${
                      currentPage === 1
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    Anterior
                  </button>
                  
                  <span className="text-sm text-gray-700">
                    Página {currentPage} de {totalPages}
                  </span>
                  
                  <button
                    onClick={() => setCurrentPage(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    className={`px-4 py-2 text-sm font-medium rounded-md ${
                      currentPage === totalPages
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    Siguiente
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default RQPage;
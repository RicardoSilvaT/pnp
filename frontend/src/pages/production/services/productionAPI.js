// src/pages/production/services/productionAPI.js


import config from '../../../config/env.js';

const API_BASE_URL = `http://${config.API_HOST}:8000/api/production`;

// Función mejorada para obtener CSRF token
const getCsrfToken = () => {
  // Primero intentar obtener de las cookies
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'csrftoken') {
      return value;
    }
  }
  
  // Si no hay cookie, intentar obtener del meta tag
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) {
    return meta.getAttribute('content');
  }
  
  return '';
};

// Función para obtener CSRF token del servidor
const fetchCsrfToken = async () => {
  try {
    const response = await fetch(`http://${config.API_HOST}:8000/admin/`, {
      credentials: 'include',
    });
    // Después de esta llamada, el CSRF token debería estar en las cookies
    return getCsrfToken();
  } catch (error) {
    console.warn('No se pudo obtener CSRF token:', error);
    return '';
  }
};

// Función auxiliar para manejar respuestas
const handleResponse = async (response) => {
  if (!response.ok) {
    let errorMessage = `Error ${response.status}: ${response.statusText}`;
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorData.message || errorMessage;
    } catch (e) {
      // Si no se puede parsear el JSON, usar el mensaje por defecto
    }
    throw new Error(errorMessage);
  }
  
  const data = await response.json();
  
  // Si la respuesta tiene paginación (results), extraer solo los resultados
  if (data && typeof data === 'object' && data.results && Array.isArray(data.results)) {
    console.log(`📄 Respuesta paginada: ${data.results.length} de ${data.count} registros`);
    return data.results; // Retornar solo el array de resultados
  }
  
  // Si es un array directo, retornarlo tal como está
  if (Array.isArray(data)) {
    console.log(`📋 Array directo: ${data.length} registros`);
    return data;
  }
  
  // Si es un objeto único, retornarlo tal como está
  console.log(`📄 Objeto único:`, typeof data);
  return data;
};

// Función auxiliar para hacer requests con autenticación
const fetchWithAuth = async (url, options = {}) => {
  console.log('🌐 Haciendo request a:', url);
  
  const defaultOptions = {
    credentials: 'include', // Incluir cookies de sesión
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Para métodos que modifican datos, obtener CSRF token
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(options.method)) {
    let csrfToken = getCsrfToken();
    
    // Si no hay token, intentar obtenerlo del servidor
    if (!csrfToken) {
      console.log('🔒 Obteniendo CSRF token...');
      csrfToken = await fetchCsrfToken();
    }
    
    if (csrfToken) {
      defaultOptions.headers['X-CSRFToken'] = csrfToken;
      console.log('🔑 CSRF token agregado');
    } else {
      console.warn('⚠️ No se pudo obtener CSRF token');
    }
  }

  try {
    const response = await fetch(url, defaultOptions);
    console.log(`📡 Respuesta de ${url}:`, response.status, response.statusText);
    const data = await handleResponse(response);
    console.log(`✅ Datos procesados de ${url}:`, Array.isArray(data) ? `${data.length} registros` : 'objeto único');
    return data;
  } catch (error) {
    console.error(`❌ Error en ${url}:`, error);
    throw error;
  }
};

// =============================================================================
// APIs DE TABLAS DE REFERENCIA
// =============================================================================

export const referenceAPI = {
  // Ubicación
  getDepartamentos: () => {
    console.log('🏛️ Obteniendo departamentos...');
    return fetchWithAuth(`${API_BASE_URL}/reference/departamentos/`);
  },
  
  getProvinciasByDepartamento: (departamentoId) => {
    console.log('🏛️ Obteniendo provincias para departamento:', departamentoId);
    return fetchWithAuth(`${API_BASE_URL}/reference/provincias/por_departamento/?departamento_id=${departamentoId}`);
  },
  
  getDistritosByProvincia: (provinciaId) => {
    console.log('🏛️ Obteniendo distritos para provincia:', provinciaId);
    return fetchWithAuth(`${API_BASE_URL}/reference/distritos/por_provincia/?provincia_id=${provinciaId}`);
  },

  // Personas
  getNacionalidades: () => {
    console.log('🌍 Obteniendo nacionalidades...');
    return fetchWithAuth(`${API_BASE_URL}/reference/nacionalidades/`);
  },
  
  getTiposDocumento: () => {
    console.log('📄 Obteniendo tipos de documento...');
    return fetchWithAuth(`${API_BASE_URL}/reference/tipos-documento/`);
  },
  
  getTiposRequisitoria: () => {
    console.log('⚖️ Obteniendo tipos de requisitoria...');
    return fetchWithAuth(`${API_BASE_URL}/reference/tipos-requisitoria/`);
  },

  // Delitos
  getDelitosFuero: () => {
    console.log('⚖️ Obteniendo delitos fuero...');
    return fetchWithAuth(`${API_BASE_URL}/reference/delitos-fuero/`);
  },
  
  getDelitosGeneralByFuero: (fueroId) => {
    console.log('⚖️ Obteniendo delitos generales para fuero:', fueroId);
    return fetchWithAuth(`${API_BASE_URL}/reference/delitos-general/por_fuero/?fuero_id=${fueroId}`);
  },
  
  getDelitosEspecificoByGeneral: (generalId) => {
    console.log('⚖️ Obteniendo delitos específicos para general:', generalId);
    return fetchWithAuth(`${API_BASE_URL}/reference/delitos-especifico/por_general/?general_id=${generalId}`);
  },
  
  getDelitosSubtipoByEspecifico: (especificoId) => {
    console.log('⚖️ Obteniendo delitos subtipos para específico:', especificoId);
    return fetchWithAuth(`${API_BASE_URL}/reference/delitos-subtipo/por_especifico/?especifico_id=${especificoId}`);
  },

  // Estructura Policial
  getDireccionesPoliciales: () => {
    console.log('🚔 Obteniendo direcciones policiales...');
    return fetchWithAuth(`${API_BASE_URL}/reference/direcciones-policiales/`);
  },
  
  getDireccionesEspecializadasByDireccion: (direccionId) => {
    console.log('🚔 Obteniendo direcciones especializadas para dirección:', direccionId);
    return fetchWithAuth(`${API_BASE_URL}/reference/direcciones-especializadas/por_direccion/?direccion_id=${direccionId}`);
  },
  
  getDivisionesPoliciales: () => {
    console.log('🚔 Obteniendo divisiones policiales...');
    return fetchWithAuth(`${API_BASE_URL}/reference/divisiones-policiales/`);
  },
  
  getDepartamentosPoliciales: () => {
    console.log('🚔 Obteniendo departamentos policiales...');
    return fetchWithAuth(`${API_BASE_URL}/reference/departamentos-policiales/`);
  },
  
  getUnidadesPoliciales: () => {
    console.log('🚔 Obteniendo unidades policiales...');
    return fetchWithAuth(`${API_BASE_URL}/reference/unidades-policiales/`);
  },

  // Armas
  getCategoriasArmas: () => {
    console.log('🔫 Obteniendo categorías de armas...');
    return fetchWithAuth(`${API_BASE_URL}/reference/categorias-armas/`);
  },
  
  getTiposArmasByCategoria: (categoriaId) => {
    console.log('🔫 Obteniendo tipos de arma para categoría:', categoriaId);
    return fetchWithAuth(`${API_BASE_URL}/reference/tipos-armas/por_categoria/?categoria_id=${categoriaId}`);
  },

  // Judicial
  getSituacionesDetenido: () => {
    console.log('⚖️ Obteniendo situaciones de detenido...');
    return fetchWithAuth(`${API_BASE_URL}/reference/situaciones-detenido/`);
  },
  
  getFiscalias: () => {
    console.log('⚖️ Obteniendo fiscalías...');
    return fetchWithAuth(`${API_BASE_URL}/reference/fiscalias/`);
  },

  // Filtro cascada global
  getFiltrosCascada: (tipo, padreId) => {
    console.log('🔗 Obteniendo filtros cascada:', tipo, padreId);
    return fetchWithAuth(`${API_BASE_URL}/filtros-cascada/?tipo=${tipo}&padre_id=${padreId}`);
  },
};

// =============================================================================
// APIs DE FORMULARIOS DE PERSONAS
// =============================================================================

// Función especial para manejar respuestas de formularios (que siempre tienen paginación)
const fetchFormularioWithAuth = async (url, options = {}) => {
  console.log('📋 Haciendo request a formulario:', url);
  
  const defaultOptions = {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(options.method)) {
    let csrfToken = getCsrfToken();
    
    if (!csrfToken) {
      console.log('🔒 Obteniendo CSRF token para formulario...');
      csrfToken = await fetchCsrfToken();
    }
    
    if (csrfToken) {
      defaultOptions.headers['X-CSRFToken'] = csrfToken;
      console.log('🔑 CSRF token agregado al formulario');
    }
  }

  try {
    const response = await fetch(url, defaultOptions);
    console.log(`📡 Respuesta de formulario ${url}:`, response.status, response.statusText);
    
    if (!response.ok) {
      let errorMessage = `Error ${response.status}: ${response.statusText}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
        // Si hay errores de validación específicos, incluirlos
        if (errorData.errors) {
          errorMessage += '\n' + JSON.stringify(errorData.errors, null, 2);
        }
      } catch (e) {
        // Si no se puede parsear el JSON, usar el mensaje por defecto
      }
      throw new Error(errorMessage);
    }
    
    const data = await response.json();
    console.log(`✅ Datos de formulario procesados:`, data);
    return data; // Para formularios, retornar el objeto completo con paginación
  } catch (error) {
    console.error(`❌ Error en formulario ${url}:`, error);
    throw error;
  }
};

// API para RQ (Requisitorias)
export const rqAPI = {
  // CRUD básico
  getAll: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    console.log('📋 Obteniendo lista de RQ...');
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/rq/${queryString ? `?${queryString}` : ''}`);
  },
  
  getById: (id) => {
    console.log('📋 Obteniendo RQ por ID:', id);
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/rq/${id}/`);
  },
  
  create: (data) => {
    console.log('📋 Creando nuevo RQ...', data);
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/rq/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
  
  update: (id, data) => {
    console.log('📋 Actualizando RQ:', id);
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/rq/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },
  
  partialUpdate: (id, data) => {
    console.log('📋 Actualización parcial de RQ:', id);
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/rq/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },
  
  delete: (id) => {
    console.log('📋 Eliminando RQ:', id);
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/rq/${id}/`, {
      method: 'DELETE',
    });
  },

  // Endpoints especiales
  getEstadisticas: () => {
    console.log('📊 Obteniendo estadísticas de RQ...');
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/rq/estadisticas/`);
  },
  
  getEstadisticasRQ: () => {
    console.log('📊 Obteniendo estadísticas específicas de RQ...');
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/rq/estadisticas_rq/`);
  },
  
  buscarPorDocumento: (numeroDocumento) => {
    console.log('🔍 Buscando RQ por documento:', numeroDocumento);
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/rq/buscar_por_documento/?numero_documento=${numeroDocumento}`);
  },
  
  busquedaAvanzada: (params) => {
    console.log('🔍 Búsqueda avanzada de RQ...');
    const queryString = new URLSearchParams(params).toString();
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/rq/busqueda_avanzada/?${queryString}`);
  },
};

// Resto de las APIs (detenidos y menores) mantienen la misma estructura...
export const detenidosAPI = {
  getAll: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/detenidos/${queryString ? `?${queryString}` : ''}`);
  },
  getById: (id) => fetchFormularioWithAuth(`${API_BASE_URL}/personas/detenidos/${id}/`),
  create: (data) => fetchFormularioWithAuth(`${API_BASE_URL}/personas/detenidos/`, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => fetchFormularioWithAuth(`${API_BASE_URL}/personas/detenidos/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => fetchFormularioWithAuth(`${API_BASE_URL}/personas/detenidos/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (id) => fetchFormularioWithAuth(`${API_BASE_URL}/personas/detenidos/${id}/`, { method: 'DELETE' }),
  getEstadisticas: () => fetchFormularioWithAuth(`${API_BASE_URL}/personas/detenidos/estadisticas/`),
  getEstadisticasDetenidos: () => fetchFormularioWithAuth(`${API_BASE_URL}/personas/detenidos/estadisticas_detenidos/`),
  buscarPorOrganizacion: (nombreOrganizacion) => fetchFormularioWithAuth(`${API_BASE_URL}/personas/detenidos/buscar_por_organizacion/?nombre_organizacion=${nombreOrganizacion}`),
  busquedaAvanzada: (params) => {
    const queryString = new URLSearchParams(params).toString();
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/detenidos/busqueda_avanzada/?${queryString}`);
  },
};

export const menoresAPI = {
  getAll: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/menores/${queryString ? `?${queryString}` : ''}`);
  },
  getById: (id) => fetchFormularioWithAuth(`${API_BASE_URL}/personas/menores/${id}/`),
  create: (data) => fetchFormularioWithAuth(`${API_BASE_URL}/personas/menores/`, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => fetchFormularioWithAuth(`${API_BASE_URL}/personas/menores/${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
  partialUpdate: (id, data) => fetchFormularioWithAuth(`${API_BASE_URL}/personas/menores/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (id) => fetchFormularioWithAuth(`${API_BASE_URL}/personas/menores/${id}/`, { method: 'DELETE' }),
  getEstadisticas: () => fetchFormularioWithAuth(`${API_BASE_URL}/personas/menores/estadisticas/`),
  getEstadisticasMenores: () => fetchFormularioWithAuth(`${API_BASE_URL}/personas/menores/estadisticas_menores/`),
  getReporteMenoresRiesgo: () => fetchFormularioWithAuth(`${API_BASE_URL}/personas/menores/reporte_menores_riesgo/`),
  busquedaAvanzada: (params) => {
    const queryString = new URLSearchParams(params).toString();
    return fetchFormularioWithAuth(`${API_BASE_URL}/personas/menores/busqueda_avanzada/?${queryString}`);
  },
};

// Exportar todas las APIs
export default {
  reference: referenceAPI,
  rq: rqAPI,
  detenidos: detenidosAPI,
  menores: menoresAPI,
};
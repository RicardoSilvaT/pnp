import config from '../config/env.js';

// src/services/groupService.js
const API_BASE_URL = `http://${config.API_HOST}:8000/api/`;


class IncidentService {
  async getAll() {
    const token = localStorage.getItem('access_token');
    let allResults = [];
    let nextUrl = `${API_BASE_URL}list/`;

    while (nextUrl) {
      const response = await fetch(nextUrl, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorBody = await response.json();
        const error = new Error('Error al obtener incidencias');
        error.responseData = errorBody;
        throw error;
      }

      const data = await response.json();
      allResults = [...allResults, ...data.results];
      nextUrl = data.next;
    }

    console.log("Todos los datos:", allResults);
    return allResults;
  }

  async uploadExcel(file) {
    const token = localStorage.getItem('access_token');
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}upload/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });

    const result = await response.json();

    if (!response.ok || !Array.isArray(result?.datos)) {
      const error = new Error('Error al subir el archivo');
      error.responseData = result;
      throw error;
    }

    return result; // importante: devuelve el objeto completo con .datos
  }

  /**
   * Elimina todos los registros proporcionados en la lista de IDs.
   * @param {Array<number>} ids - Array de IDs a eliminar.
   * @returns {Promise<Object>} - Resultado del servidor.
   */
  async deleteBatch(ids) {
    const token = localStorage.getItem('access_token');
    const response = await fetch(`${API_BASE_URL}delete-batch/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ ids }),
    });

    const result = await response.json();
    if (!response.ok) {
      const error = new Error(result.error || 'Error al eliminar registros');
      error.responseData = result;
      throw error;
    }

    return result;
  }
}

export default new IncidentService();

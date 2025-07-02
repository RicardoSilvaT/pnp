import { useState } from 'react';
import incidentService from '../services/incidentService';

export const useIncident = () => {
  const [incidents, setIncidents] = useState([]);
  const [lastBatchIds, setLastBatchIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchIncidents = async () => {
    try {
      setLoading(true);
      const data = await incidentService.getAll();
      setIncidents(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || 'Error al obtener los datos');
    } finally {
      setLoading(false);
    }
  };

  const uploadIncidents = async (file) => {
    try {
      setLoading(true);
      const response = await incidentService.uploadExcel(file);
      console.log("Respuesta del servidor:", response);

      const nuevosDatos = Array.isArray(response?.datos) ? response.datos : [];
      if (nuevosDatos.length === 0) {
        throw new Error("No se encontraron registros cargados.");
      }

      setIncidents(nuevosDatos);
      const ids = nuevosDatos.map(item => item.id);
      setLastBatchIds(ids);
      return nuevosDatos;
    } catch (err) {
      console.error("Error en la carga:", err);
      let mensaje = "Error desconocido";
      if (err.responseData) {
        mensaje = err.responseData.error || JSON.stringify(err.responseData);
      } else if (err.message) {
        mensaje = err.message;
      }
      setError(mensaje);
      return [];
    } finally {
      setLoading(false);
    }
  };

  const deleteLastBatch = async () => {
    try {
      setLoading(true);
      if (!lastBatchIds.length) throw new Error("No hay registros de la última carga para eliminar.");
      const resp = await incidentService.deleteBatch(lastBatchIds);
      await fetchIncidents();
      return resp;
    } catch (err) {
      setError(err.message || 'Error al eliminar registros');
      return null;
    } finally {
      setLoading(false);
    }
  };

  return {
    incidents,
    loading,
    error,
    lastBatchIds,
    refetch: fetchIncidents,
    uploadIncidents,
    deleteLastBatch,
    setIncidents,
  };
};

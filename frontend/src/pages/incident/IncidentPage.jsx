import React, { useState, useRef } from 'react';
import { useIncident } from '../../hooks/useIncident';
import incidentService from '../../services/incidentService';
import Button from '../../Components/common/Button';

const IncidentPage = () => {
  const [file, setFile] = useState(null);
  const fileInputRef = useRef();
  const [lastFileSignature, setLastFileSignature] = useState(null);

  const {
    incidents,
    uploadIncidents,
    refetch,
    loading,
    lastBatchIds,
    deleteLastBatch
  } = useIncident();

  const [excelData, setExcelData] = useState([]);
  const [showAll, setShowAll] = useState(false);

  // Filtrado
  const [filterField, setFilterField] = useState('creado_por');
  const [filterValue, setFilterValue] = useState('');
  const [filteredData, setFilteredData] = useState([]);

  const handleFileClick = () => {
    if (fileInputRef.current) fileInputRef.current.value = null;
  };

  const handleUpload = async () => {
    if (!file) return;
    const newSignature = `${file.name}-${file.size}-${file.lastModified}`;
    if (newSignature === lastFileSignature && !window.confirm('¿Reintentar con el mismo archivo?')) {
      return;
    }
    const nuevos = await uploadIncidents(file);
    setExcelData(nuevos);
    setShowAll(false);
    setLastFileSignature(newSignature);
    setFile(null);
    setFilteredData([]);
  };

  const handleVerTodos = async () => {
    await refetch();
    setShowAll(true);
    setFilteredData([]);
  };

  const handleDeleteLast = async () => {
    if (!lastBatchIds.length) {
      return alert('No hay registros de la última carga.');
    }
    if (!window.confirm('¿Eliminar toda la última carga?')) return;
    const resp = await deleteLastBatch();
    if (resp?.mensaje) alert(resp.mensaje);
    await refetch();
    setShowAll(true);
    setFilteredData([]);
  };

  const handleFilter = () => {
    const source = showAll ? incidents : excelData;
    if (!filterValue) {
      setFilteredData([]);
      return;
    }
    const lower = filterValue.toLowerCase();
    setFilteredData(
      source.filter(item =>
        String(item[filterField] ?? '').toLowerCase().includes(lower)
      )
    );
  };

  const handleClearFilter = () => {
    setFilterValue('');
    setFilteredData([]);
  };

  const handleDeleteFiltered = async () => {
    const toDelete = filteredData.length ? filteredData : [];
    if (!toDelete.length) {
      return alert('No hay registros filtrados.');
    }
    if (!window.confirm('¿Eliminar todos los registros filtrados?')) return;
    const ids = toDelete.map(i => i.id);
    const resp = await incidentService.deleteBatch(ids);
    if (resp?.mensaje) alert(resp.mensaje);
    await refetch();
    setShowAll(true);
    setFilteredData([]);
  };

  // Datos a mostrar en tabla
  const datosAMostrar = filteredData.length
    ? filteredData
    : showAll
      ? incidents
      : excelData;

  // Columnas (omitimos coordenadas)
  const columnas = [
    'ID', 'ID Doc Denuncia', 'Libro', 'N° Denuncia', 'Tipo Denuncia',
    'Situación Denuncia', 'Tipo', 'Subtipo', 'Modalidad',
    'Fecha Hecho', 'Hora Hecho', 'Departamento', 'Provincia', 'Distrito',
    'Tipo Vía', 'Ubicación', 'Cuadra', 'DNI', 'Apellido Paterno',
    'Apellido Materno', 'Nombre', 'Situación Persona',
    'Fecha Nacimiento', 'Hora Nacimiento', 'Edad', 'Sexo',
    'Estado Civil', 'Grado Instrucción', 'Ocupación', 'País Natal',
    'Región', 'Comisaría', 'Fecha Registro', 'Hora Registro',
    'Creado Por', 'Fecha Carga'
  ];

  // Formato Lima local
  const formatLocalDateTime = iso => {
    if (!iso) return '';
    const s = iso.endsWith('Z') || iso.includes('+') ? iso : iso + 'Z';
    const d = new Date(s);
    const fecha = d.toLocaleDateString('es-PE', {
      day: '2-digit', month: '2-digit', year: 'numeric', timeZone: 'America/Lima'
    });
    const hora = d.toLocaleTimeString('es-PE', {
      hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'America/Lima'
    });
    return `${fecha} ${hora}`;
  };

  return (
    <div className="max-w-7xl mx-auto p-4 space-y-4">
      {/* HEADER */}
      <div className="sticky top-0 z-40 bg-white shadow rounded-lg p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-800">Incidencias Delictivas</h1>
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 w-full sm:w-auto">
          <label
            htmlFor="file"
            onClick={handleFileClick}
            className="flex-1 sm:flex-none px-4 py-2 bg-white border border-gray-300 rounded text-center cursor-pointer hover:bg-gray-50"
          >
            Seleccionar Excel
          </label>
          <input
            id="file"
            type="file"
            accept=".xlsx"
            ref={fileInputRef}
            onChange={e => setFile(e.target.files[0])}
            className="hidden"
          />
          <Button className="w-full sm:w-auto" onClick={handleUpload}>Subir</Button>
        </div>
      </div>

      {/* FILTROS */}
      <div className="sticky top-[88px] z-30 bg-white border border-gray-200 rounded-lg p-4 flex flex-col md:flex-row flex-wrap gap-3 items-start md:items-center shadow-sm">
        <Button className="w-full md:w-auto" variant="secondary" onClick={handleVerTodos}>Ver todos</Button>
        <Button className="w-full md:w-auto" variant="danger" onClick={handleDeleteLast}>Eliminar última carga</Button>

        <select
          value={filterField}
          onChange={e => setFilterField(e.target.value)}
          className="border border-gray-300 rounded p-2 w-full md:w-auto"
        >
          {columnas.map(col => (
            <option
              key={col}
              value={col.toLowerCase().replace(/\s|\//g, '_')}
            >
              {col}
            </option>
          ))}
        </select>

        <input
          type="text"
          value={filterValue}
          onChange={e => setFilterValue(e.target.value)}
          placeholder="Valor de filtro"
          className="border border-gray-300 rounded p-2 flex-1 min-w-[150px] w-full md:w-auto"
        />

        <div className="flex flex-col sm:flex-row gap-2 w-full sm:w-auto">
          <Button variant="primary" className="w-full sm:w-auto" onClick={handleFilter}>Filtrar</Button>
          <Button variant="secondary" className="w-full sm:w-auto" onClick={handleClearFilter}>Limpiar</Button>
          <Button variant="danger" className="w-full sm:w-auto" onClick={handleDeleteFiltered}>Eliminar filtrados</Button>
        </div>
      </div>

      {/* TABLA */}
      <div className="bg-white border border-gray-200 rounded-lg p-4 overflow-x-auto overflow-y-auto max-h-[60vh]">
        {loading ? (
          <p className="text-center py-10 text-gray-500">Cargando...</p>
        ) : datosAMostrar.length === 0 ? (
          <p className="text-center py-10 text-gray-400">No hay registros para mostrar.</p>
        ) : (
          <table className="min-w-full text-left border-collapse">
            <thead>
              <tr>
                {columnas.map((h, i) => (
                  <th
                    key={i}
                    className="sticky top-0 bg-gray-50 px-4 py-3 sm:py-4 text-gray-700 font-bold text-sm sm:text-base border-b z-10"
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {datosAMostrar.map(item => (
                <tr key={item.id} className="hover:bg-gray-50">
                  {[
                    item.id,
                    item.id_doc_denuncia,
                    item.libro,
                    item.num_denuncia,
                    item.tipodenuncia,
                    item.situaciondenuncia,
                    item.tipo,
                    item.subtipo,
                    item.modalidad,
                    item.fec_hecho_fecha,
                    item.fec_hecho_hora,
                    item.dpto,
                    item.prov,
                    item.distrito,
                    item.tipovia,
                    item.ubicacion,
                    item.cuadra,
                    item.dni,
                    item.apellido_paterno,
                    item.apellido_materno,
                    item.nombre,
                    item.situacionpersona,
                    item.fec_nacimiento_fecha,
                    item.fec_nacimiento_hora,
                    item.edad,
                    item.sexo,
                    item.estadocivil,
                    item.gradoinstruccion,
                    item.ocupacion,
                    item.pais_natal,
                    item.region,
                    item.descripcioncomisaria,
                    item.fec_registro_fecha,
                    item.fec_registro_hora,
                    item.creado_por,
                    formatLocalDateTime(item.fecha_carga)
                  ].map((val, j) => (
                    <td
                      key={j}
                      className="px-4 py-2 text-sm sm:text-base border-b text-gray-700"
                    >
                      {val ?? '-'}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default IncidentPage;

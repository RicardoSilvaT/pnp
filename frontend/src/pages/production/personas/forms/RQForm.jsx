import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { 
  DocumentTextIcon, 
  UserIcon, 
  MapPinIcon,
  BuildingOfficeIcon,
  ShieldCheckIcon,
  ScaleIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import { rqAPI, referenceAPI } from '../../services/productionAPI';

// =============================================================================
// COMPONENTES FUERA DEL COMPONENTE PRINCIPAL (IMPORTANTE)
// =============================================================================

// Componente de campo de entrada
const InputField = ({ label, name, type = 'text', required = false, disabled = false, value, onChange, errors, ...props }) => (
  <div className="space-y-1">
    <label className="block text-sm font-medium text-gray-700">
      {label}
      {required && <span className="text-red-500 ml-1">*</span>}
    </label>
    <input
      type={type}
      name={name}
      value={value || ''}
      onChange={onChange}
      disabled={disabled}
      className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-red-500 focus:border-transparent ${
        errors[name] ? 'border-red-300' : 'border-gray-300'
      } ${disabled ? 'bg-gray-100' : ''}`}
      {...props}
    />
    {errors[name] && (
      <p className="text-sm text-red-600">{errors[name]}</p>
    )}
  </div>
);

// Componente de select
const SelectField = ({ label, name, options, required = false, disabled = false, placeholder = 'Seleccionar...', value, onChange, errors }) => {
  // Validación más robusta
  const validOptions = Array.isArray(options) ? options : [];
  
  return (
    <div className="space-y-1">
      <label className="block text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <select
        name={name}
        value={value || ''}
        onChange={onChange}
        disabled={disabled}
        className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-red-500 focus:border-transparent ${
          errors[name] ? 'border-red-300' : 'border-gray-300'
        } ${disabled ? 'bg-gray-100' : ''}`}
      >
        <option value="">{placeholder}</option>
        {validOptions.map((option) => (
          <option key={option.id} value={option.id}>
            {option.nombre}
          </option>
        ))}
      </select>
      {errors[name] && (
        <p className="text-sm text-red-600">{errors[name]}</p>
      )}
    </div>
  );
};

// Componente de textarea
const TextareaField = ({ label, name, required = false, disabled = false, rows = 3, value, onChange, errors, ...props }) => (
  <div className="space-y-1">
    <label className="block text-sm font-medium text-gray-700">
      {label}
      {required && <span className="text-red-500 ml-1">*</span>}
    </label>
    <textarea
      name={name}
      value={value || ''}
      onChange={onChange}
      disabled={disabled}
      rows={rows}
      className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-red-500 focus:border-transparent ${
        errors[name] ? 'border-red-300' : 'border-gray-300'
      } ${disabled ? 'bg-gray-100' : ''}`}
      {...props}
    />
    {errors[name] && (
      <p className="text-sm text-red-600">{errors[name]}</p>
    )}
  </div>
);

// =============================================================================
// COMPONENTE PRINCIPAL
// =============================================================================

const RQForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditing = !!id;

  // Estados del formulario
  const [formData, setFormData] = useState({
    // Datos básicos
    fecha_detencion: '',
    hora_detencion: '',
    
    // Datos de la persona
    apellido_paterno: '',
    apellido_materno: '',
    nombres: '',
    edad: '',
    genero: '',
    nacionalidad: '',
    tipo_documento: '',
    numero_documento: '',
    
    // Ubicación
    departamento: '',
    provincia: '',
    distrito: '',
    
    // Requisitoria
    tipo_requisitoria: '',
    esta_en_lista_mas_buscados: 'NO',
    
    // Funcionario público
    es_funcionario_publico: 'PARTICULARES',
    entidad_publica: '',
    detalle_entidad: '',
    
    // Delito principal
    es_tentativa: 'NO',
    delito_fuero: '',
    delito_general: '',
    delito_especifico: '',
    delito_subtipo: '',
    
    // Delito secundario
    es_tentativa_2: 'NO',
    delito_fuero_2: '',
    delito_general_2: '',
    delito_especifico_2: '',
    delito_subtipo_2: '',
    
    // Unidad policial
    direccion_policial: '',
    direccion_especializada: '',
    division_policial: '',
    departamento_policial: '',
    unidad_policial: '',
    
    // Información judicial
    autoridad_que_solicita: '',
    documento_que_solicita: '',
    nota_informativa_sicpip: '',
    tipo_intervencion: ''
  });

  // Estados para opciones de selects
  const [opciones, setOpciones] = useState({
    departamentos: [],
    provincias: [],
    distritos: [],
    nacionalidades: [],
    tipos_documento: [],
    tipos_requisitoria: [],
    delitos_fuero: [],
    delitos_general: [],
    delitos_especifico: [],
    delitos_subtipo: [],
    delitos_general_2: [],
    delitos_especifico_2: [],
    delitos_subtipo_2: [],
    direcciones_policiales: [],
    direcciones_especializadas: [],
    divisiones_policiales: [],
    departamentos_policiales: [],
    unidades_policiales: []
  });

  // Estados de control
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [showDelitoSecundario, setShowDelitoSecundario] = useState(false);

  // Cargar datos iniciales
  useEffect(() => {
    loadInitialData();
    if (isEditing) {
      loadRQData();
    }
  }, [id]);

  // Cargar datos de referencia
  const loadInitialData = async () => {
    try {
      setLoading(true);
      console.log('Cargando datos iniciales...');
      
      const [
        departamentos,
        nacionalidades,
        tipos_documento,
        tipos_requisitoria,
        delitos_fuero,
        direcciones_policiales,
        divisiones_policiales,
        departamentos_policiales,
        unidades_policiales
      ] = await Promise.all([
        referenceAPI.getDepartamentos(),
        referenceAPI.getNacionalidades(),
        referenceAPI.getTiposDocumento(),
        referenceAPI.getTiposRequisitoria(),
        referenceAPI.getDelitosFuero(),
        referenceAPI.getDireccionesPoliciales(),
        referenceAPI.getDivisionesPoliciales(),
        referenceAPI.getDepartamentosPoliciales(),
        referenceAPI.getUnidadesPoliciales()
      ]);

      console.log('Datos cargados:', {
        departamentos: departamentos.length,
        nacionalidades: nacionalidades.length,
        tipos_documento: tipos_documento.length,
        tipos_requisitoria: tipos_requisitoria.length,
        delitos_fuero: delitos_fuero.length
      });

      setOpciones(prev => ({
        ...prev,
        departamentos,
        nacionalidades,
        tipos_documento,
        tipos_requisitoria,
        delitos_fuero,
        direcciones_policiales,
        divisiones_policiales,
        departamentos_policiales,
        unidades_policiales
      }));
    } catch (error) {
      console.error('Error loading initial data:', error);
      setErrors({ general: 'Error al cargar datos iniciales: ' + error.message });
    } finally {
      setLoading(false);
    }
  };

  // Cargar datos del RQ para edición
  const loadRQData = async () => {
    try {
      setLoading(true);
      const rqData = await rqAPI.getById(id);
      setFormData(rqData);
      
      // Cargar datos cascada si existen
      if (rqData.departamento) {
        loadProvincias(rqData.departamento);
      }
      if (rqData.provincia) {
        loadDistritos(rqData.provincia);
      }
      if (rqData.delito_fuero) {
        loadDelitosGeneral(rqData.delito_fuero);
      }
      if (rqData.delito_general) {
        loadDelitosEspecifico(rqData.delito_general);
      }
      if (rqData.delito_especifico) {
        loadDelitosSubtipo(rqData.delito_especifico);
      }
      if (rqData.direccion_policial) {
        loadDireccionesEspecializadas(rqData.direccion_policial);
      }
      
      // Verificar si hay delito secundario
      setShowDelitoSecundario(rqData.es_tentativa_2 === 'SÍ');
      
    } catch (error) {
      console.error('Error loading RQ data:', error);
      setErrors({ general: 'Error al cargar datos del RQ: ' + error.message });
    } finally {
      setLoading(false);
    }
  };

  // Handlers para filtros cascada
  const loadProvincias = async (departamentoId) => {
    if (!departamentoId) return;
    try {
      console.log('Cargando provincias para departamento:', departamentoId);
      const provincias = await referenceAPI.getProvinciasByDepartamento(departamentoId);
      console.log('Provincias cargadas:', provincias.length);
      setOpciones(prev => ({ ...prev, provincias }));
    } catch (error) {
      console.error('Error loading provincias:', error);
    }
  };

  const loadDistritos = async (provinciaId) => {
    if (!provinciaId) return;
    try {
      console.log('Cargando distritos para provincia:', provinciaId);
      const distritos = await referenceAPI.getDistritosByProvincia(provinciaId);
      console.log('Distritos cargados:', distritos.length);
      setOpciones(prev => ({ ...prev, distritos }));
    } catch (error) {
      console.error('Error loading distritos:', error);
    }
  };

  const loadDelitosGeneral = async (fueroId) => {
    if (!fueroId) return;
    try {
      console.log('Cargando delitos generales para fuero:', fueroId);
      const delitos = await referenceAPI.getDelitosGeneralByFuero(fueroId);
      console.log('Delitos generales cargados:', delitos.length);
      setOpciones(prev => ({ ...prev, delitos_general: delitos }));
    } catch (error) {
      console.error('Error loading delitos general:', error);
    }
  };

  const loadDelitosEspecifico = async (generalId) => {
    if (!generalId) return;
    try {
      console.log('Cargando delitos específicos para general:', generalId);
      const delitos = await referenceAPI.getDelitosEspecificoByGeneral(generalId);
      console.log('Delitos específicos cargados:', delitos.length);
      setOpciones(prev => ({ ...prev, delitos_especifico: delitos }));
    } catch (error) {
      console.error('Error loading delitos específico:', error);
    }
  };

  const loadDelitosSubtipo = async (especificoId) => {
    if (!especificoId) return;
    try {
      console.log('Cargando delitos subtipos para específico:', especificoId);
      const delitos = await referenceAPI.getDelitosSubtipoByEspecifico(especificoId);
      console.log('Delitos subtipos cargados:', delitos.length);
      setOpciones(prev => ({ ...prev, delitos_subtipo: delitos }));
    } catch (error) {
      console.error('Error loading delitos subtipo:', error);
    }
  };

  const loadDireccionesEspecializadas = async (direccionId) => {
    if (!direccionId) return;
    try {
      console.log('Cargando direcciones especializadas para dirección:', direccionId);
      const direcciones = await referenceAPI.getDireccionesEspecializadasByDireccion(direccionId);
      console.log('Direcciones especializadas cargadas:', direcciones.length);
      setOpciones(prev => ({ ...prev, direcciones_especializadas: direcciones }));
    } catch (error) {
      console.error('Error loading direcciones especializadas:', error);
    }
  };

  // Cargar datos para delito secundario
  const loadDelitosGeneral2 = async (fueroId) => {
    if (!fueroId) return;
    try {
      const delitos = await referenceAPI.getDelitosGeneralByFuero(fueroId);
      setOpciones(prev => ({ ...prev, delitos_general_2: delitos }));
    } catch (error) {
      console.error('Error loading delitos general 2:', error);
    }
  };

  const loadDelitosEspecifico2 = async (generalId) => {
    if (!generalId) return;
    try {
      const delitos = await referenceAPI.getDelitosEspecificoByGeneral(generalId);
      setOpciones(prev => ({ ...prev, delitos_especifico_2: delitos }));
    } catch (error) {
      console.error('Error loading delitos específico 2:', error);
    }
  };

  const loadDelitosSubtipo2 = async (especificoId) => {
    if (!especificoId) return;
    try {
      const delitos = await referenceAPI.getDelitosSubtipoByEspecifico(especificoId);
      setOpciones(prev => ({ ...prev, delitos_subtipo_2: delitos }));
    } catch (error) {
      console.error('Error loading delitos subtipo 2:', error);
    }
  };

  // Handler para cambios en el formulario
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Limpiar errores del campo
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }

    // Manejar filtros cascada
    if (name === 'departamento') {
      setFormData(prev => ({ ...prev, provincia: '', distrito: '' }));
      setOpciones(prev => ({ ...prev, provincias: [], distritos: [] }));
      if (value) loadProvincias(value);
    }
    
    if (name === 'provincia') {
      setFormData(prev => ({ ...prev, distrito: '' }));
      setOpciones(prev => ({ ...prev, distritos: [] }));
      if (value) loadDistritos(value);
    }
    
    // Delito principal
    if (name === 'delito_fuero') {
      setFormData(prev => ({ 
        ...prev, 
        delito_general: '', 
        delito_especifico: '', 
        delito_subtipo: '' 
      }));
      setOpciones(prev => ({ 
        ...prev, 
        delitos_general: [], 
        delitos_especifico: [], 
        delitos_subtipo: [] 
      }));
      if (value) loadDelitosGeneral(value);
    }
    
    if (name === 'delito_general') {
      setFormData(prev => ({ ...prev, delito_especifico: '', delito_subtipo: '' }));
      setOpciones(prev => ({ ...prev, delitos_especifico: [], delitos_subtipo: [] }));
      if (value) loadDelitosEspecifico(value);
    }
    
    if (name === 'delito_especifico') {
      setFormData(prev => ({ ...prev, delito_subtipo: '' }));
      setOpciones(prev => ({ ...prev, delitos_subtipo: [] }));
      if (value) loadDelitosSubtipo(value);
    }

    // Delito secundario
    if (name === 'delito_fuero_2') {
      setFormData(prev => ({ 
        ...prev, 
        delito_general_2: '', 
        delito_especifico_2: '', 
        delito_subtipo_2: '' 
      }));
      setOpciones(prev => ({ 
        ...prev, 
        delitos_general_2: [], 
        delitos_especifico_2: [], 
        delitos_subtipo_2: [] 
      }));
      if (value) loadDelitosGeneral2(value);
    }
    
    if (name === 'delito_general_2') {
      setFormData(prev => ({ ...prev, delito_especifico_2: '', delito_subtipo_2: '' }));
      setOpciones(prev => ({ ...prev, delitos_especifico_2: [], delitos_subtipo_2: [] }));
      if (value) loadDelitosEspecifico2(value);
    }
    
    if (name === 'delito_especifico_2') {
      setFormData(prev => ({ ...prev, delito_subtipo_2: '' }));
      setOpciones(prev => ({ ...prev, delitos_subtipo_2: [] }));
      if (value) loadDelitosSubtipo2(value);
    }
    
    if (name === 'direccion_policial') {
      setFormData(prev => ({ ...prev, direccion_especializada: '' }));
      setOpciones(prev => ({ ...prev, direcciones_especializadas: [] }));
      if (value) loadDireccionesEspecializadas(value);
    }

    // Mostrar/ocultar delito secundario
    if (name === 'es_tentativa_2') {
      setShowDelitoSecundario(value === 'SÍ');
      if (value === 'NO') {
        setFormData(prev => ({
          ...prev,
          delito_fuero_2: '',
          delito_general_2: '',
          delito_especifico_2: '',
          delito_subtipo_2: ''
        }));
        setOpciones(prev => ({
          ...prev,
          delitos_general_2: [],
          delitos_especifico_2: [],
          delitos_subtipo_2: []
        }));
      }
    }
  };

  // Validaciones
  const validateForm = () => {
    const newErrors = {};
    
    // Validaciones básicas
    if (!formData.fecha_detencion) newErrors.fecha_detencion = 'La fecha es obligatoria';
    if (!formData.hora_detencion) newErrors.hora_detencion = 'La hora es obligatoria';
    if (!formData.apellido_paterno) newErrors.apellido_paterno = 'El apellido paterno es obligatorio';
    if (!formData.apellido_materno) newErrors.apellido_materno = 'El apellido materno es obligatorio';
    if (!formData.nombres) newErrors.nombres = 'Los nombres son obligatorios';
    if (!formData.edad) newErrors.edad = 'La edad es obligatoria';
    if (!formData.genero) newErrors.genero = 'El género es obligatorio';
    if (!formData.nacionalidad) newErrors.nacionalidad = 'La nacionalidad es obligatoria';
    if (!formData.tipo_documento) newErrors.tipo_documento = 'El tipo de documento es obligatorio';
    if (!formData.numero_documento) newErrors.numero_documento = 'El número de documento es obligatorio';
    if (!formData.departamento) newErrors.departamento = 'El departamento es obligatorio';
    if (!formData.provincia) newErrors.provincia = 'La provincia es obligatoria';
    if (!formData.distrito) newErrors.distrito = 'El distrito es obligatorio';
    if (!formData.tipo_requisitoria) newErrors.tipo_requisitoria = 'El tipo de requisitoria es obligatorio';
    
    // Validaciones de funcionario público
    if (formData.es_funcionario_publico !== 'PARTICULARES' && !formData.entidad_publica) {
      newErrors.entidad_publica = 'La entidad pública es obligatoria';
    }
    
    // Validaciones de delito principal
    if (!formData.delito_fuero) newErrors.delito_fuero = 'El fuero es obligatorio';
    if (!formData.delito_general) newErrors.delito_general = 'El delito general es obligatorio';
    if (!formData.delito_especifico) newErrors.delito_especifico = 'El delito específico es obligatorio';
    if (!formData.delito_subtipo) newErrors.delito_subtipo = 'El subtipo es obligatorio';
    
    // Validaciones de unidad policial
    if (!formData.direccion_policial) newErrors.direccion_policial = 'La dirección policial es obligatoria';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handler para envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    try {
      setLoading(true);
      
      if (isEditing) {
        await rqAPI.update(id, formData);
      } else {
        await rqAPI.create(formData);
      }
      
      navigate('/ofad/produccion/personas/rq');
    } catch (error) {
      console.error('Error saving RQ:', error);
      setErrors({ 
        general: 'Error al guardar: ' + (error.message || 'Error desconocido') 
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading && !isEditing) {
    return (
      <div className="flex justify-center items-center min-h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
      </div>
    );
  }

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
              <h1 className="text-2xl font-bold text-gray-900">
                {isEditing ? 'Editar RQ' : 'Nuevo RQ'}
              </h1>
              <p className="text-gray-600">Persona detenida por requisitoria</p>
            </div>
          </div>
          <button
            type="button"
            onClick={() => navigate('/ofad/produccion/personas/rq')}
            className="flex items-center space-x-2 text-gray-600 hover:text-gray-800"
          >
            <XMarkIcon className="h-5 w-5" />
            <span>Cancelar</span>
          </button>
        </div>
      </div>

      {/* Mensajes de error general */}
      {errors.general && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex items-center">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-400 mr-2" />
            <p className="text-red-800">{errors.general}</p>
          </div>
        </div>
      )}

      {/* Debug info */}
      {process.env.NODE_ENV === 'development' && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
          <p className="text-sm">
            <strong>Debug:</strong> Departamentos: {opciones.departamentos.length}, 
            Nacionalidades: {opciones.nacionalidades.length},
            Loading: {loading.toString()}
          </p>
        </div>
      )}

      {/* Formulario */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Información Básica */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center space-x-2 mb-4">
            <DocumentTextIcon className="h-5 w-5 text-gray-600" />
            <h2 className="text-lg font-semibold text-gray-900">Información Básica</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <InputField
              label="Fecha de Detención"
              name="fecha_detencion"
              type="date"
              required
              value={formData.fecha_detencion}
              onChange={handleInputChange}
              errors={errors}
            />
            <InputField
              label="Hora de Detención"
              name="hora_detencion"
              type="time"
              required
              value={formData.hora_detencion}
              onChange={handleInputChange}
              errors={errors}
            />
          </div>
        </div>

        {/* Datos de la Persona */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center space-x-2 mb-4">
            <UserIcon className="h-5 w-5 text-gray-600" />
            <h2 className="text-lg font-semibold text-gray-900">Datos de la Persona</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <InputField
              label="Apellido Paterno"
              name="apellido_paterno"
              required
              value={formData.apellido_paterno}
              onChange={handleInputChange}
              errors={errors}
            />
            <InputField
              label="Apellido Materno"
              name="apellido_materno"
              required
              value={formData.apellido_materno}
              onChange={handleInputChange}
              errors={errors}
            />
            <InputField
              label="Nombres"
              name="nombres"
              required
              value={formData.nombres}
              onChange={handleInputChange}
              errors={errors}
            />
            <InputField
              label="Edad"
              name="edad"
              type="number"
              min="0"
              max="120"
              required
              value={formData.edad}
              onChange={handleInputChange}
              errors={errors}
            />
            <SelectField
              label="Género"
              name="genero"
              options={[
                { id: 'MASCULINO', nombre: 'MASCULINO' },
                { id: 'FEMENINO', nombre: 'FEMENINO' }
              ]}
              required
              value={formData.genero}
              onChange={handleInputChange}
              errors={errors}
            />
            <SelectField
              label="Nacionalidad"
              name="nacionalidad"
              options={opciones.nacionalidades}
              required
              value={formData.nacionalidad}
              onChange={handleInputChange}
              errors={errors}
            />
            <SelectField
              label="Tipo de Documento"
              name="tipo_documento"
              options={opciones.tipos_documento}
              required
              value={formData.tipo_documento}
              onChange={handleInputChange}
              errors={errors}
            />
            <InputField
              label="Número de Documento"
              name="numero_documento"
              required
              value={formData.numero_documento}
              onChange={handleInputChange}
              errors={errors}
            />
          </div>
        </div>

        {/* Ubicación */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center space-x-2 mb-4">
            <MapPinIcon className="h-5 w-5 text-gray-600" />
            <h2 className="text-lg font-semibold text-gray-900">Lugar de Detención</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <SelectField
              label="Departamento"
              name="departamento"
              options={opciones.departamentos}
              required
              value={formData.departamento}
              onChange={handleInputChange}
              errors={errors}
            />
            <SelectField
              label="Provincia"
              name="provincia"
              options={opciones.provincias}
              disabled={!formData.departamento}
              required
              value={formData.provincia}
              onChange={handleInputChange}
              errors={errors}
            />
            <SelectField
              label="Distrito"
              name="distrito"
options={opciones.distritos}
             disabled={!formData.provincia}
             required
             value={formData.distrito}
             onChange={handleInputChange}
             errors={errors}
           />
         </div>
       </div>

       {/* Información de Requisitoria */}
       <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
         <div className="flex items-center space-x-2 mb-4">
           <ScaleIcon className="h-5 w-5 text-gray-600" />
           <h2 className="text-lg font-semibold text-gray-900">Información de Requisitoria</h2>
         </div>
         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
           <SelectField
             label="Tipo de Requisitoria"
             name="tipo_requisitoria"
             options={opciones.tipos_requisitoria}
             required
             value={formData.tipo_requisitoria}
             onChange={handleInputChange}
             errors={errors}
           />
           <SelectField
             label="¿Está en lista de más buscados?"
             name="esta_en_lista_mas_buscados"
             options={[
               { id: 'SÍ', nombre: 'SÍ' },
               { id: 'NO', nombre: 'NO' }
             ]}
             required
             value={formData.esta_en_lista_mas_buscados}
             onChange={handleInputChange}
             errors={errors}
           />
         </div>
       </div>

       {/* Información Laboral */}
       <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
         <div className="flex items-center space-x-2 mb-4">
           <BuildingOfficeIcon className="h-5 w-5 text-gray-600" />
           <h2 className="text-lg font-semibold text-gray-900">Información Laboral</h2>
         </div>
         <div className="space-y-4">
           <SelectField
             label="¿Es funcionario público?"
             name="es_funcionario_publico"
             options={[
               { id: 'PARTICULARES', nombre: 'PARTICULARES' },
               { id: 'FUNCIONARIO PUBLICO', nombre: 'FUNCIONARIO PUBLICO' },
               { id: 'SERVIDOR PUBLICO', nombre: 'SERVIDOR PUBLICO' },
               { id: 'EX FUNCIONARIO PUBLICO', nombre: 'EX FUNCIONARIO PUBLICO' },
               { id: 'EX SERVIDOR PUBLICO', nombre: 'EX SERVIDOR PUBLICO' }
             ]}
             required
             value={formData.es_funcionario_publico}
             onChange={handleInputChange}
             errors={errors}
           />
           {formData.es_funcionario_publico !== 'PARTICULARES' && (
             <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
               <TextareaField
                 label="Entidad Pública"
                 name="entidad_publica"
                 required
                 value={formData.entidad_publica}
                 onChange={handleInputChange}
                 errors={errors}
               />
               <TextareaField
                 label="Detalle de Entidad"
                 name="detalle_entidad"
                 value={formData.detalle_entidad}
                 onChange={handleInputChange}
                 errors={errors}
               />
             </div>
           )}
         </div>
       </div>

       {/* Delito Principal */}
       <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
         <div className="flex items-center space-x-2 mb-4">
           <ScaleIcon className="h-5 w-5 text-gray-600" />
           <h2 className="text-lg font-semibold text-gray-900">Delito Principal</h2>
         </div>
         <div className="space-y-4">
           <SelectField
             label="¿Es tentativa?"
             name="es_tentativa"
             options={[
               { id: 'SÍ', nombre: 'SÍ' },
               { id: 'NO', nombre: 'NO' }
             ]}
             required
             value={formData.es_tentativa}
             onChange={handleInputChange}
             errors={errors}
           />
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
             <SelectField
               label="Fuero/Leyes Especiales"
               name="delito_fuero"
               options={opciones.delitos_fuero}
               required
               value={formData.delito_fuero}
               onChange={handleInputChange}
               errors={errors}
             />
             <SelectField
               label="Delito General"
               name="delito_general"
               options={opciones.delitos_general}
               disabled={!formData.delito_fuero}
               required
               value={formData.delito_general}
               onChange={handleInputChange}
               errors={errors}
             />
             <SelectField
               label="Delito Específico"
               name="delito_especifico"
               options={opciones.delitos_especifico}
               disabled={!formData.delito_general}
               required
               value={formData.delito_especifico}
               onChange={handleInputChange}
               errors={errors}
             />
             <SelectField
               label="Sub Tipo"
               name="delito_subtipo"
               options={opciones.delitos_subtipo}
               disabled={!formData.delito_especifico}
               required
               value={formData.delito_subtipo}
               onChange={handleInputChange}
               errors={errors}
             />
           </div>
         </div>
       </div>

       {/* Delito Secundario */}
       <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
         <div className="flex items-center space-x-2 mb-4">
           <ScaleIcon className="h-5 w-5 text-gray-600" />
           <h2 className="text-lg font-semibold text-gray-900">Delito Secundario</h2>
         </div>
         <div className="space-y-4">
           <SelectField
             label="¿Hay delito secundario?"
             name="es_tentativa_2"
             options={[
               { id: 'SÍ', nombre: 'SÍ' },
               { id: 'NO', nombre: 'NO' }
             ]}
             value={formData.es_tentativa_2}
             onChange={handleInputChange}
             errors={errors}
           />
           {showDelitoSecundario && (
             <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
               <SelectField
                 label="Fuero/Leyes Especiales 2"
                 name="delito_fuero_2"
                 options={opciones.delitos_fuero}
                 value={formData.delito_fuero_2}
                 onChange={handleInputChange}
                 errors={errors}
               />
               <SelectField
                 label="Delito General 2"
                 name="delito_general_2"
                 options={opciones.delitos_general_2}
                 disabled={!formData.delito_fuero_2}
                 value={formData.delito_general_2}
                 onChange={handleInputChange}
                 errors={errors}
               />
               <SelectField
                 label="Delito Específico 2"
                 name="delito_especifico_2"
                 options={opciones.delitos_especifico_2}
                 disabled={!formData.delito_general_2}
                 value={formData.delito_especifico_2}
                 onChange={handleInputChange}
                 errors={errors}
               />
               <SelectField
                 label="Sub Tipo 2"
                 name="delito_subtipo_2"
                 options={opciones.delitos_subtipo_2}
                 disabled={!formData.delito_especifico_2}
                 value={formData.delito_subtipo_2}
                 onChange={handleInputChange}
                 errors={errors}
               />
             </div>
           )}
         </div>
       </div>

       {/* Unidad Policial */}
       <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
         <div className="flex items-center space-x-2 mb-4">
           <ShieldCheckIcon className="h-5 w-5 text-gray-600" />
           <h2 className="text-lg font-semibold text-gray-900">Unidad Policial</h2>
         </div>
         <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
           <SelectField
             label="Dirección - DIRNIC/DIRNOS"
             name="direccion_policial"
             options={opciones.direcciones_policiales}
             required
             value={formData.direccion_policial}
             onChange={handleInputChange}
             errors={errors}
           />
           <SelectField
             label="Dirección Especializada/Región/Frente"
             name="direccion_especializada"
             options={opciones.direcciones_especializadas}
             disabled={!formData.direccion_policial}
             value={formData.direccion_especializada}
             onChange={handleInputChange}
             errors={errors}
           />
           <SelectField
             label="División Policial"
             name="division_policial"
             options={opciones.divisiones_policiales}
             value={formData.division_policial}
             onChange={handleInputChange}
             errors={errors}
           />
           <SelectField
             label="Departamento Policial"
             name="departamento_policial"
             options={opciones.departamentos_policiales}
             value={formData.departamento_policial}
             onChange={handleInputChange}
             errors={errors}
           />
           <SelectField
             label="Unidad/Área/Equipo"
             name="unidad_policial"
             options={opciones.unidades_policiales}
             value={formData.unidad_policial}
             onChange={handleInputChange}
             errors={errors}
           />
         </div>
       </div>

       {/* Información Judicial */}
       <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
         <div className="flex items-center space-x-2 mb-4">
           <ScaleIcon className="h-5 w-5 text-gray-600" />
           <h2 className="text-lg font-semibold text-gray-900">Información Judicial</h2>
         </div>
         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
           <TextareaField
             label="Autoridad que Solicita"
             name="autoridad_que_solicita"
             value={formData.autoridad_que_solicita}
             onChange={handleInputChange}
             errors={errors}
           />
           <TextareaField
             label="Documento que Solicita"
             name="documento_que_solicita"
             value={formData.documento_que_solicita}
             onChange={handleInputChange}
             errors={errors}
           />
         </div>
       </div>

       {/* Información Adicional */}
       <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
         <div className="flex items-center space-x-2 mb-4">
           <DocumentTextIcon className="h-5 w-5 text-gray-600" />
           <h2 className="text-lg font-semibold text-gray-900">Información Adicional</h2>
         </div>
         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
           <TextareaField
             label="Nota Informativa SICPIP"
             name="nota_informativa_sicpip"
             rows={4}
             value={formData.nota_informativa_sicpip}
             onChange={handleInputChange}
             errors={errors}
           />
           <SelectField
             label="Tipo de Intervención"
             name="tipo_intervencion"
             options={[
               { id: 'OPERATIVO', nombre: 'OPERATIVO' },
               { id: 'INTERVENCIÓN', nombre: 'INTERVENCIÓN' }
             ]}
             value={formData.tipo_intervencion}
             onChange={handleInputChange}
             errors={errors}
           />
         </div>
       </div>

       {/* Botones de acción */}
       <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
         <div className="flex items-center justify-end space-x-4">
           <button
             type="button"
             onClick={() => navigate('/ofad/produccion/personas/rq')}
             className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:ring-2 focus:ring-gray-500 focus:border-transparent"
             disabled={loading}
           >
             Cancelar
           </button>
           <button
             type="submit"
             disabled={loading}
             className="flex items-center space-x-2 px-6 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
           >
             {loading ? (
               <>
                 <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                 <span>Guardando...</span>
               </>
             ) : (
               <>
                 <CheckCircleIcon className="h-4 w-4" />
                 <span>{isEditing ? 'Actualizar RQ' : 'Crear RQ'}</span>
               </>
             )}
           </button>
         </div>
       </div>
     </form>
   </div>
 );
};

export default RQForm;
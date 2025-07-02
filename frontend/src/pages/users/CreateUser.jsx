// src/pages/users/CreateUser.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, User, Mail, Phone, Lock, Users, Shield } from 'lucide-react';
import { useUsers } from '../../hooks/useUsers';
import { useGroups } from '../../hooks/useGroups';
import Button from '../../Components/common/Button';

const CreateUser = () => {
  const navigate = useNavigate();
  const { createUser } = useUsers();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (userData) => {
    setLoading(true);
    try {
      const newUser = await createUser(userData);
      alert('Usuario creado exitosamente');
      navigate('/users');
    } catch (error) {
      alert('Error al crear usuario: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/users');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-green-50 to-emerald-50">
      <div className="max-w-full xl:max-w-6xl mx-auto px-4 md:px-6 py-6 md:py-8">
        
        {/* Header Section */}
        <section className="mb-8 md:mb-10">
          <div className="max-w-4xl mx-auto">
            <div className="flex flex-col md:flex-row items-start md:items-center gap-4 md:gap-6 mb-6">
              <Button
                variant="outline"
                onClick={handleCancel}
                className="bg-white hover:bg-gray-50 border-2 border-green-200 hover:border-green-300 text-green-700 hover:text-green-800 px-4 md:px-6 py-2 md:py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 font-semibold"
              >
                <ArrowLeft size={20} className="mr-2" />
                Volver
              </Button>
              
              <div className="text-center md:text-left flex-1">
                <h1 className="text-3xl md:text-5xl font-black bg-gradient-to-r from-green-700 via-green-600 to-amber-600 bg-clip-text text-transparent mb-2 md:mb-4 tracking-tight">
                  Crear Nuevo Usuario
                </h1>
                <div className="flex items-center justify-center md:justify-start">
                  <div className="w-1 h-6 bg-gradient-to-b from-green-600 to-amber-500 rounded-full mr-3"></div>
                  <p className="text-gray-700 text-base md:text-lg font-medium">
                    Completa el formulario para crear un nuevo usuario
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Form Container */}
        <section>
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl border border-green-100 overflow-hidden">
              <div className="bg-gradient-to-r from-green-600 to-emerald-600 px-6 md:px-8 py-4 md:py-6">
                <div className="flex items-center justify-center">
                  <User className="h-6 w-6 text-white mr-3" />
                  <h2 className="text-xl md:text-2xl font-bold text-white">Información del Usuario</h2>
                </div>
              </div>
              
              <div className="p-6 md:p-8">
                <UserFormContent
                  onSubmit={handleSubmit}
                  onCancel={handleCancel}
                  loading={loading}
                />
              </div>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
};

// Validadores separados para reducir complejidad
const validateRequiredFields = (formData) => {
  const errors = {};
  const requiredFields = [
    { field: 'username', message: 'El nombre de usuario es requerido' },
    { field: 'email', message: 'El email es requerido' },
    { field: 'first_name', message: 'El nombre es requerido' },
    { field: 'last_name', message: 'El apellido es requerido' },
    { field: 'dni', message: 'El DNI es requerido' },
    { field: 'password', message: 'La contraseña es requerida' },
    { field: 'group', message: 'Debe seleccionar un grupo' }
  ];

  requiredFields.forEach(({ field, message }) => {
    if (!formData[field] || !formData[field].toString().trim()) {
      errors[field] = message;
    }
  });

  return errors;
};

const validateFormats = (formData) => {
  const errors = {};

  // Validación de DNI
  if (formData.dni && !/^\d{8}$/.test(formData.dni.trim())) {
    errors.dni = 'El DNI debe tener exactamente 8 números';
  }

  // Validación de email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (formData.email && !emailRegex.test(formData.email)) {
    errors.email = 'El formato del email no es válido';
  }

  return errors;
};

const validatePhoneCreate = (formData, users) => {
  const errors = {};
  
  if (formData.phone && formData.phone.trim() !== '') {
    const phoneValue = formData.phone.trim();
    if (!/^\d{9}$/.test(phoneValue)) {
      errors.phone = 'El teléfono debe tener exactamente 9 números';
    } else if (users && users.some(u => u.phone === phoneValue)) {
      errors.phone = 'Este número de teléfono ya está en uso';
    }
  }
  
  return errors;
};

const validatePasswordCreate = (formData) => {
  const errors = {};
  
  if (formData.password && formData.password.length < 8) {
    errors.password = 'La contraseña debe tener al menos 8 caracteres';
  }

  if (formData.password && formData.password !== formData.confirm_password) {
    errors.confirm_password = 'Las contraseñas no coinciden';
  }
  
  return errors;
};

const prepareCreateData = (formData) => {
  const submitData = { ...formData };
  delete submitData.confirm_password;

  // Manejar phone - enviar null si está vacío
  if (!submitData.phone || submitData.phone.trim() === '') {
    delete submitData.phone;
  } else {
    submitData.phone = submitData.phone.trim();
  }

  return submitData;
};

// Hook personalizado para obtener opciones de grupos
const useGroupOptions = () => {
  const { groups, loading: groupsLoading } = useGroups();
  
  // Grupos predeterminados
  const defaultGroups = [
    { value: 'analista', label: 'Analista' },
    { value: 'administrador', label: 'Administrador' },
    { value: 'visualizador', label: 'Visualizador' }
  ];

  // Combinar grupos predeterminados con grupos creados dinámicamente
  const groupOptions = React.useMemo(() => {
    const options = [{ value: '', label: 'Seleccionar grupo...' }];
    
    // Agregar grupos predeterminados
    options.push(...defaultGroups);
    
    // Agregar grupos dinámicos si existen y no están ya en los predeterminados
    if (groups && Array.isArray(groups)) {
      const defaultGroupValues = defaultGroups.map(g => g.value.toLowerCase());
      
      groups.forEach(group => {
        // Usar la estructura que devuelve tu API
        const groupValue = group.name?.toLowerCase() || group.value?.toLowerCase();
        const groupLabel = group.name || group.label || group.value;
        
        // Solo agregar si no está en los grupos predeterminados
        if (groupValue && !defaultGroupValues.includes(groupValue)) {
          options.push({
            value: groupValue,
            label: groupLabel
          });
        }
      });
    }
    
    return options;
  }, [groups]);

  return { groupOptions, groupsLoading };
};

// Componente del formulario refactorizado
const UserFormContent = ({ onSubmit, onCancel, loading }) => {
  const { users } = useUsers();
  const { groupOptions, groupsLoading } = useGroupOptions();
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    dni: '',
    phone: '',
    password: '',
    confirm_password: '',
    is_active: true,
    group: '',
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;
    
    setFormData(prev => ({
      ...prev,
      [name]: newValue
    }));

    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const requiredErrors = validateRequiredFields(formData);
    const formatErrors = validateFormats(formData);
    const phoneErrors = validatePhoneCreate(formData, users);
    const passwordErrors = validatePasswordCreate(formData);

    const allErrors = {
      ...requiredErrors,
      ...formatErrors,
      ...phoneErrors,
      ...passwordErrors
    };

    setErrors(allErrors);
    return Object.keys(allErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validateForm()) {
      return;
    }

    const submitData = prepareCreateData(formData);
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-8" autoComplete="on">
      
      {/* Información Personal */}
      <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-xl border-l-4 border-green-500">
        <div className="flex items-center mb-4">
          <User className="h-5 w-5 text-green-600 mr-2" />
          <h3 className="text-lg font-bold text-green-800">Información Personal</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* First Name */}
          <div>
            <label htmlFor="create-first-name" className="block text-sm font-bold text-gray-700 mb-2">
              Nombre *
            </label>
            <input
              type="text"
              id="create-first-name"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              autoComplete="given-name"
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 focus:ring-green-200 transition-all duration-300 shadow-md hover:shadow-lg ${
                errors.first_name 
                  ? 'border-red-400 focus:border-red-500' 
                  : 'border-green-200 focus:border-green-500'
              }`}
              placeholder="Juan"
            />
            {errors.first_name && (
              <p className="mt-2 text-sm text-red-600 font-medium">{errors.first_name}</p>
            )}
          </div>

          {/* Last Name */}
          <div>
            <label htmlFor="create-last-name" className="block text-sm font-bold text-gray-700 mb-2">
              Apellido *
            </label>
            <input
              type="text"
              id="create-last-name"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              autoComplete="family-name"
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 focus:ring-green-200 transition-all duration-300 shadow-md hover:shadow-lg ${
                errors.last_name 
                  ? 'border-red-400 focus:border-red-500' 
                  : 'border-green-200 focus:border-green-500'
              }`}
              placeholder="Pérez"
            />
            {errors.last_name && (
              <p className="mt-2 text-sm text-red-600 font-medium">{errors.last_name}</p>
            )}
          </div>

          {/* DNI */}
          <div>
            <label htmlFor="create-dni" className="block text-sm font-bold text-gray-700 mb-2">
              DNI *
            </label>
            <input
              type="text"
              id="create-dni"
              name="dni"
              value={formData.dni}
              onChange={handleChange}
              autoComplete="off"
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 focus:ring-green-200 transition-all duration-300 shadow-md hover:shadow-lg ${
                errors.dni 
                  ? 'border-red-400 focus:border-red-500' 
                  : 'border-green-200 focus:border-green-500'
              }`}
              placeholder="12345678"
            />
            {errors.dni && (
              <p className="mt-2 text-sm text-red-600 font-medium">{errors.dni}</p>
            )}
          </div>

          {/* Phone */}
          <div>
            <label htmlFor="create-phone" className="block text-sm font-bold text-gray-700 mb-2">
              <Phone className="h-4 w-4 inline mr-1" />
              Teléfono
            </label>
            <input
              type="tel"
              id="create-phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              autoComplete="tel"
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 focus:ring-green-200 transition-all duration-300 shadow-md hover:shadow-lg ${
                errors.phone 
                  ? 'border-red-400 focus:border-red-500' 
                  : 'border-green-200 focus:border-green-500'
              }`}
              placeholder="999999999"
            />
            {errors.phone && (
              <p className="mt-2 text-sm text-red-600 font-medium">{errors.phone}</p>
            )}
          </div>
        </div>
      </div>

      {/* Información de Cuenta */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl border-l-4 border-blue-500">
        <div className="flex items-center mb-4">
          <Mail className="h-5 w-5 text-blue-600 mr-2" />
          <h3 className="text-lg font-bold text-blue-800">Información de Cuenta</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Username */}
          <div>
            <label htmlFor="create-username" className="block text-sm font-bold text-gray-700 mb-2">
              Nombre de Usuario *
            </label>
            <input
              type="text"
              id="create-username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              autoComplete="username"
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-200 transition-all duration-300 shadow-md hover:shadow-lg ${
                errors.username 
                  ? 'border-red-400 focus:border-red-500' 
                  : 'border-blue-200 focus:border-blue-500'
              }`}
              placeholder="nombre_usuario"
            />
            {errors.username && (
              <p className="mt-2 text-sm text-red-600 font-medium">{errors.username}</p>
            )}
          </div>

          {/* Email */}
          <div>
            <label htmlFor="create-email" className="block text-sm font-bold text-gray-700 mb-2">
              <Mail className="h-4 w-4 inline mr-1" />
              Email *
            </label>
            <input
              type="email"
              id="create-email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              autoComplete="email"
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-200 transition-all duration-300 shadow-md hover:shadow-lg ${
                errors.email 
                  ? 'border-red-400 focus:border-red-500' 
                  : 'border-blue-200 focus:border-blue-500'
              }`}
              placeholder="usuario@ejemplo.com"
            />
            {errors.email && (
              <p className="mt-2 text-sm text-red-600 font-medium">{errors.email}</p>
            )}
          </div>
        </div>
      </div>

      {/* Seguridad */}
      <div className="bg-gradient-to-r from-amber-50 to-orange-50 p-6 rounded-xl border-l-4 border-amber-500">
        <div className="flex items-center mb-4">
          <Lock className="h-5 w-5 text-amber-600 mr-2" />
          <h3 className="text-lg font-bold text-amber-800">Seguridad</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Password */}
          <div>
            <label htmlFor="create-password" className="block text-sm font-bold text-gray-700 mb-2">
              Contraseña *
            </label>
            <input
              type="password"
              id="create-password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              autoComplete="new-password"
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 focus:ring-amber-200 transition-all duration-300 shadow-md hover:shadow-lg ${
                errors.password 
                  ? 'border-red-400 focus:border-red-500' 
                  : 'border-amber-200 focus:border-amber-500'
              }`}
              placeholder="Mínimo 8 caracteres"
            />
            {errors.password && (
              <p className="mt-2 text-sm text-red-600 font-medium">{errors.password}</p>
            )}
          </div>

          {/* Confirm Password */}
          <div>
            <label htmlFor="create-confirm-password" className="block text-sm font-bold text-gray-700 mb-2">
              Confirmar Contraseña *
            </label>
            <input
              type="password"
              id="create-confirm-password"
              name="confirm_password"
              value={formData.confirm_password}
              onChange={handleChange}
              autoComplete="new-password"
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 focus:ring-amber-200 transition-all duration-300 shadow-md hover:shadow-lg ${
                errors.confirm_password 
                  ? 'border-red-400 focus:border-red-500' 
                  : 'border-amber-200 focus:border-amber-500'
              }`}
              placeholder="Repetir contraseña"
            />
            {errors.confirm_password && (
              <p className="mt-2 text-sm text-red-600 font-medium">{errors.confirm_password}</p>
            )}
          </div>
        </div>
      </div>

      {/* Grupo y Estado */}
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl border-l-4 border-purple-500">
        <div className="flex items-center mb-4">
          <Shield className="h-5 w-5 text-purple-600 mr-2" />
          <h3 className="text-lg font-bold text-purple-800">Grupo y Estado</h3>
        </div>
        <div className="space-y-6">
          {/* Group Selection */}
          <div>
            <label htmlFor="create-group" className="block text-sm font-bold text-gray-700 mb-2">
              <Users className="h-4 w-4 inline mr-1" />
              Grupo *
            </label>
            <select
              id="create-group"
              name="group"
              value={formData.group}
              onChange={handleChange}
              disabled={groupsLoading}
              autoComplete="off"
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 focus:ring-purple-200 transition-all duration-300 shadow-md hover:shadow-lg bg-white ${
                errors.group 
                  ? 'border-red-400 focus:border-red-500' 
                  : 'border-purple-200 focus:border-purple-500'
              } ${groupsLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {groupOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            {groupsLoading && (
              <p className="mt-2 text-sm text-gray-500">Cargando grupos...</p>
            )}
            {errors.group && (
              <p className="mt-2 text-sm text-red-600 font-medium">{errors.group}</p>
            )}
            <p className="mt-2 text-xs text-gray-500">
              Selecciona el grupo que define los permisos del usuario
            </p>
          </div>

          {/* Active Status */}
          <label className="flex items-center p-4 bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 border border-purple-100 cursor-pointer">
            <input
              id="create_is_active"
              name="is_active"
              type="checkbox"
              checked={formData.is_active}
              onChange={handleChange}
              className="h-5 w-5 text-green-600 focus:ring-green-500 border-2 border-gray-300 rounded-md"
            />
            <span className="ml-3 flex items-center">
              <Users className="h-4 w-4 text-green-600 mr-2" />
              <span className="text-sm font-bold text-gray-900">Usuario activo</span>
            </span>
          </label>
        </div>
      </div>

      {/* Form Actions */}
      <div className="flex flex-col sm:flex-row justify-end gap-4 pt-6 border-t-2 border-gray-100">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={loading || groupsLoading}
          className="w-full sm:w-auto bg-white hover:bg-gray-50 border-2 border-gray-300 hover:border-gray-400 text-gray-700 hover:text-gray-800 px-6 py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 font-semibold"
        >
          Cancelar
        </Button>
        <Button
          type="submit"
          variant="primary"
          loading={loading}
          disabled={loading || groupsLoading}
          className="w-full sm:w-auto bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white px-8 py-3 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 font-semibold text-lg"
        >
          {loading ? 'Creando...' : 'Crear Usuario'}
        </Button>
      </div>
    </form>
  );
};

export default CreateUser;
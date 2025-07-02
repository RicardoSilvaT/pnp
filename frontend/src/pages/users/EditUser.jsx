// src/pages/users/EditUser.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, User, Mail, Phone, Lock, Users, Shield, Clock, Hash, Calendar } from 'lucide-react';
import { useUser, useUsers } from '../../hooks/useUsers';
import { useFormValidation } from '../../hooks/useFormValidation';
import Button from '../../Components/common/Button';
import FormField from '../../Components/common/FormField';

const EditUser = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { user, loading: userLoading, error } = useUser(id);
  const { updateUser } = useUsers();
  const { errors, validateForm, clearError } = useFormValidation(true); // true = isEditing
  
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
  
  const [loading, setLoading] = useState(false);

  // Grupos predeterminados (como en el código original)
  const groupOptions = [
    { value: '', label: 'Seleccionar grupo...' },
    { value: 'analista', label: 'Analista' },
    { value: 'administrador', label: 'Administrador' },
    { value: 'visualizador', label: 'Visualizador' }
  ];

  // Llenar formulario con datos del usuario
  useEffect(() => {
    if (user) {
      setFormData({
        username: user.username || '',
        email: user.email || '',
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        dni: user.dni || '',
        phone: user.phone || '',
        password: '',
        confirm_password: '',
        is_active: user.is_active,
        group: user.group_frontend || user.group_name?.toLowerCase() || '',
      });
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));

    if (errors[name]) {
      clearError(name);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm(formData)) {
      return;
    }

    setLoading(true);
    try {
      const submitData = prepareSubmitData(formData);
      await updateUser(id, submitData);
      alert('Usuario actualizado exitosamente');
      navigate('/users');
    } catch (error) {
      alert('Error al actualizar usuario: ' + (error.message || 'Error desconocido'));
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => navigate('/users');

  // Estados de carga y error
  if (userLoading) return <LoadingState />;
  if (error) return <ErrorState error={error} onBack={handleCancel} />;
  if (!user) return <NotFoundState onBack={handleCancel} />;

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-green-50 to-emerald-50">
      <div className="max-w-full xl:max-w-6xl mx-auto px-4 md:px-6 py-6 md:py-8">
        
        <PageHeader user={user} onBack={handleCancel} />
        
        <section>
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl border border-green-100 overflow-hidden">
              <FormHeader />
              <div className="p-6 md:p-8">
                <EditUserForm
                  user={user}
                  formData={formData}
                  errors={errors}
                  loading={loading}
                  groupOptions={groupOptions}
                  onChange={handleChange}
                  onSubmit={handleSubmit}
                  onCancel={handleCancel}
                />
              </div>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
};

// Componentes extraídos pero manteniendo el diseño original
const PageHeader = ({ user, onBack }) => (
  <section className="mb-8 md:mb-10">
    <div className="max-w-4xl mx-auto">
      <div className="flex flex-col md:flex-row items-start md:items-center gap-4 md:gap-6 mb-6">
        <Button
          variant="outline"
          onClick={onBack}
          className="bg-white hover:bg-gray-50 border-2 border-green-200 hover:border-green-300 text-green-700 hover:text-green-800 px-4 md:px-6 py-2 md:py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 font-semibold"
        >
          <ArrowLeft size={20} className="mr-2" />
          Volver
        </Button>
        
        <div className="text-center md:text-left flex-1">
          <h1 className="text-3xl md:text-5xl font-black bg-gradient-to-r from-green-700 via-green-600 to-amber-600 bg-clip-text text-transparent mb-2 md:mb-4 tracking-tight">
            Editar Usuario
          </h1>
          <div className="flex items-center justify-center md:justify-start">
            <div className="w-1 h-6 bg-gradient-to-b from-green-600 to-amber-500 rounded-full mr-3"></div>
            <p className="text-gray-700 text-base md:text-lg font-medium">
              Modifica la información de {user.first_name} {user.last_name}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
);

const FormHeader = () => (
  <div className="bg-gradient-to-r from-green-600 to-emerald-600 px-6 md:px-8 py-4 md:py-6">
    <div className="flex items-center justify-center">
      <User className="h-6 w-6 text-white mr-3" />
      <h2 className="text-xl md:text-2xl font-bold text-white">Editar Información del Usuario</h2>
    </div>
  </div>
);

const EditUserForm = ({ user, formData, errors, loading, groupOptions, onChange, onSubmit, onCancel }) => (
  <form onSubmit={onSubmit} className="space-y-8">
    
    {/* Información del Usuario Actual */}
    <UserInfoSection user={user} />

    {/* Información Personal */}
    <PersonalInfoSection 
      formData={formData} 
      errors={errors} 
      onChange={onChange}
      disabled={loading}
    />

    {/* Información de Cuenta */}
    <AccountInfoSection 
      formData={formData} 
      errors={errors} 
      onChange={onChange}
      disabled={loading}
    />

    {/* Seguridad */}
    <PasswordSection 
      formData={formData} 
      errors={errors} 
      onChange={onChange}
      disabled={loading}
    />

    {/* Grupo y Estado */}
    <GroupStatusSection 
      formData={formData} 
      errors={errors} 
      onChange={onChange}
      groupOptions={groupOptions}
      disabled={loading}
    />

    <FormActions 
      onCancel={onCancel}
      loading={loading}
    />

  </form>
);

// Secciones hermosas del formulario original
const UserInfoSection = ({ user }) => (
  <div className="bg-gradient-to-r from-indigo-50 to-blue-50 p-6 rounded-xl border-l-4 border-indigo-500">
    <div className="flex items-center mb-4">
      <Hash className="h-5 w-5 text-indigo-600 mr-2" />
      <h3 className="text-lg font-bold text-indigo-800">Información del Usuario</h3>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <InfoCard 
        icon={Calendar}
        label="Creado"
        value={user.created_at ? new Date(user.created_at).toLocaleDateString('es-PE') : '-'}
      />
      <InfoCard 
        icon={Clock}
        label="Último acceso"
        value={user.last_login ? new Date(user.last_login).toLocaleDateString('es-PE') : 'Nunca'}
      />
      <InfoCard 
        icon={Hash}
        label="ID"
        value={`#${user.id}`}
      />
    </div>
  </div>
);

const InfoCard = ({ icon: Icon, label, value }) => (
  <div className="bg-white p-4 rounded-lg shadow-md">
    <div className="flex items-center mb-2">
      <Icon className="h-4 w-4 text-indigo-600 mr-2" />
      <span className="text-sm font-medium text-gray-500">{label}</span>
    </div>
    <div className="text-sm font-bold text-gray-900">{value}</div>
  </div>
);

const PersonalInfoSection = ({ formData, errors, onChange, disabled }) => (
  <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-xl border-l-4 border-green-500">
    <div className="flex items-center mb-4">
      <User className="h-5 w-5 text-green-600 mr-2" />
      <h3 className="text-lg font-bold text-green-800">Información Personal</h3>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <FormField
        id="edit-first-name"
        name="first_name"
        label="Nombre"
        value={formData.first_name}
        onChange={onChange}
        error={errors.first_name}
        placeholder="Juan"
        autoComplete="given-name"
        disabled={disabled}
        required
        variant="edituser"
      />

      <FormField
        id="edit-last-name"
        name="last_name"
        label="Apellido"
        value={formData.last_name}
        onChange={onChange}
        error={errors.last_name}
        placeholder="Pérez"
        autoComplete="family-name"
        disabled={disabled}
        required
        variant="edituser"
      />

      <FormField
        id="edit-dni"
        name="dni"
        label="DNI"
        value={formData.dni}
        onChange={onChange}
        error={errors.dni}
        placeholder="12345678"
        autoComplete="off"
        disabled={disabled}
        required
        variant="edituser"
      />

      <div>
        <label htmlFor="edit-phone" className="block text-sm font-bold text-gray-700 mb-2">
          <Phone className="h-4 w-4 inline mr-1" />
          Teléfono
        </label>
        <input
          type="text"
          id="edit-phone"
          name="phone"
          value={formData.phone}
          onChange={onChange}
          autoComplete="tel"
          disabled={disabled}
          className="w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 focus:ring-green-200 transition-all duration-300 shadow-md hover:shadow-lg border-green-200 focus:border-green-500"
          placeholder="999999999"
        />
      </div>
    </div>
  </div>
);

const AccountInfoSection = ({ formData, errors, onChange, disabled }) => (
  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl border-l-4 border-blue-500">
    <div className="flex items-center mb-4">
      <Mail className="h-5 w-5 text-blue-600 mr-2" />
      <h3 className="text-lg font-bold text-blue-800">Información de Cuenta</h3>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <FormField
        id="edit-username"
        name="username"
        label="Nombre de Usuario"
        value={formData.username}
        onChange={onChange}
        error={errors.username}
        placeholder="nombre_usuario"
        autoComplete="username"
        disabled={disabled}
        required
        variant="edituser"
        borderColor="blue"
      />

      <div>
        <label htmlFor="edit-email" className="block text-sm font-bold text-gray-700 mb-2">
          <Mail className="h-4 w-4 inline mr-1" />
          Email *
        </label>
        <input
          type="email"
          id="edit-email"
          name="email"
          value={formData.email}
          onChange={onChange}
          autoComplete="email"
          disabled={disabled}
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
);

const PasswordSection = ({ formData, errors, onChange, disabled }) => (
  <div className="bg-gradient-to-r from-amber-50 to-orange-50 p-6 rounded-xl border-l-4 border-amber-500">
    <div className="flex items-center mb-4">
      <Lock className="h-5 w-5 text-amber-600 mr-2" />
      <h3 className="text-lg font-bold text-amber-800">Cambiar Contraseña</h3>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <FormField
        id="edit-password"
        name="password"
        type="password"
        label="Nueva Contraseña"
        value={formData.password}
        onChange={onChange}
        error={errors.password}
        placeholder="Dejar vacío para mantener actual"
        autoComplete="new-password"
        disabled={disabled}
        variant="edituser"
        borderColor="amber"
      />

      {formData.password && (
        <FormField
          id="edit-confirm-password"
          name="confirm_password"
          type="password"
          label="Confirmar Nueva Contraseña"
          value={formData.confirm_password}
          onChange={onChange}
          error={errors.confirm_password}
          placeholder="Repetir nueva contraseña"
          autoComplete="new-password"
          disabled={disabled}
          required
          variant="edituser"
          borderColor="amber"
        />
      )}
    </div>
  </div>
);

const GroupStatusSection = ({ formData, errors, onChange, groupOptions, disabled }) => (
  <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl border-l-4 border-purple-500">
    <div className="flex items-center mb-4">
      <Shield className="h-5 w-5 text-purple-600 mr-2" />
      <h3 className="text-lg font-bold text-purple-800">Grupo y Estado</h3>
    </div>
    <div className="space-y-6">
      {/* Group Selection */}
      <div>
        <label htmlFor="edit-group" className="block text-sm font-bold text-gray-700 mb-2">
          <Users className="h-4 w-4 inline mr-1" />
          Grupo *
        </label>
        <select
          id="edit-group"
          name="group"
          value={formData.group}
          onChange={onChange}
          disabled={disabled}
          className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 focus:ring-purple-200 transition-all duration-300 shadow-md hover:shadow-lg bg-white ${
            errors.group 
              ? 'border-red-400 focus:border-red-500' 
              : 'border-purple-200 focus:border-purple-500'
          } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {groupOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
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
          id="edit_is_active"
          name="is_active"
          type="checkbox"
          checked={formData.is_active}
          onChange={onChange}
          disabled={disabled}
          className="h-5 w-5 text-green-600 focus:ring-green-500 border-2 border-gray-300 rounded-md"
        />
        <span className="ml-3 flex items-center">
          <Users className="h-4 w-4 text-green-600 mr-2" />
          <span className="text-sm font-bold text-gray-900">Usuario activo</span>
        </span>
      </label>
    </div>
  </div>
);

const FormActions = ({ onCancel, loading }) => (
  <div className="flex flex-col sm:flex-row justify-end gap-4 pt-6 border-t-2 border-gray-100">
    <Button
      type="button"
      variant="outline"
      onClick={onCancel}
      disabled={loading}
      className="w-full sm:w-auto bg-white hover:bg-gray-50 border-2 border-gray-300 hover:border-gray-400 text-gray-700 hover:text-gray-800 px-6 py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 font-semibold"
    >
      Cancelar
    </Button>
    <Button
      type="submit"
      variant="primary"
      loading={loading}
      disabled={loading}
      className="w-full sm:w-auto bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white px-8 py-3 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 font-semibold text-lg"
    >
      {loading ? 'Actualizando...' : 'Actualizar Usuario'}
    </Button>
  </div>
);

// Estados simples (sin cambios)
const LoadingState = () => (
  <div className="min-h-screen bg-gradient-to-br from-amber-50 via-green-50 to-emerald-50 flex items-center justify-center">
    <div className="flex flex-col items-center space-y-4">
      <div className="animate-spin rounded-full h-16 w-16 border-4 border-green-700 border-t-transparent shadow-lg"></div>
      <p className="text-green-800 font-semibold text-lg">Cargando usuario...</p>
    </div>
  </div>
);

const ErrorState = ({ error, onBack }) => (
  <div className="min-h-screen bg-gradient-to-br from-amber-50 via-green-50 to-emerald-50 p-8">
    <div className="max-w-2xl mx-auto">
      <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6 shadow-lg">
        <h3 className="text-red-800 font-semibold text-lg mb-2">Error al cargar usuario</h3>
        <p className="text-red-600 mb-4">{error}</p>
        <Button variant="outline" onClick={onBack}>
          <ArrowLeft size={16} className="mr-2" />
          Volver a usuarios
        </Button>
      </div>
    </div>
  </div>
);

const NotFoundState = ({ onBack }) => (
  <div className="min-h-screen bg-gradient-to-br from-amber-50 via-green-50 to-emerald-50 p-8">
    <div className="max-w-2xl mx-auto">
      <div className="bg-amber-50 border-2 border-amber-200 rounded-xl p-6 shadow-lg">
        <h3 className="text-amber-800 font-semibold text-lg mb-2">Usuario no encontrado</h3>
        <p className="text-amber-600 mb-4">El usuario solicitado no existe o ha sido eliminado</p>
        <Button variant="outline" onClick={onBack}>
          <ArrowLeft size={16} className="mr-2" />
          Volver a usuarios
        </Button>
      </div>
    </div>
  </div>
);

// Función auxiliar
const prepareSubmitData = (formData) => {
  const submitData = { ...formData };
  delete submitData.confirm_password;
  
  if (!submitData.password) {
    delete submitData.password;
  }
  
  return submitData;
};

export default EditUser;
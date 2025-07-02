// src/pages/groups/CreateGroup.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Shield, Lock, Check, X } from 'lucide-react';
import { useGroups, usePermissions } from '../../hooks/useGroups';
import Button from '../../Components/common/Button';

const CreateGroup = () => {
  const navigate = useNavigate();
  const { createGroup } = useGroups();
  const { permissions, loading: permissionsLoading } = usePermissions();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    permissions: []
  });
  const [errors, setErrors] = useState({});
  const [searchPermission, setSearchPermission] = useState('');
  const [selectAll, setSelectAll] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validación
    if (!formData.name.trim()) {
      setErrors({ name: 'El nombre del grupo es requerido' });
      return;
    }

    setLoading(true);
    try {
      await createGroup(formData);
      alert('Grupo creado exitosamente');
      navigate('/groups');
    } catch (error) {
      alert('Error al crear grupo: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/groups');
  };

  const handleNameChange = (e) => {
    setFormData({ ...formData, name: e.target.value });
    if (errors.name) {
      setErrors({});
    }
  };

  const handlePermissionToggle = (permissionId) => {
    setFormData(prev => ({
      ...prev,
      permissions: prev.permissions.includes(permissionId)
        ? prev.permissions.filter(id => id !== permissionId)
        : [...prev.permissions, permissionId]
    }));
  };

  const handleSelectAll = () => {
    if (selectAll) {
      setFormData({ ...formData, permissions: [] });
    } else {
      setFormData({ 
        ...formData, 
        permissions: filteredPermissions.map(p => p.id) 
      });
    }
    setSelectAll(!selectAll);
  };

  // Filtrar permisos basado en búsqueda
  const filteredPermissions = permissions.filter(permission => 
    permission.name?.toLowerCase().includes(searchPermission.toLowerCase()) ||
    permission.codename?.toLowerCase().includes(searchPermission.toLowerCase())
  );

  // Agrupar permisos por modelo/app
  const groupedPermissions = filteredPermissions.reduce((acc, permission) => {
    const parts = permission.codename?.split('_') || [];
    const model = parts.length > 1 ? parts[parts.length - 1] : 'otros';
    
    if (!acc[model]) {
      acc[model] = [];
    }
    acc[model].push(permission);
    return acc;
  }, {});

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-green-50 to-emerald-50">
      <div className="max-w-6xl mx-auto px-4 md:px-6 py-8 md:py-12">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center mb-4">
            <Button
              variant="outline"
              onClick={handleCancel}
              className="mr-4"
            >
              <ArrowLeft size={20} className="mr-2" />
              Volver
            </Button>
            <div>
              <h1 className="text-2xl md:text-3xl font-black bg-gradient-to-r from-green-700 via-green-600 to-amber-600 bg-clip-text text-transparent">
                Crear Nuevo Grupo
              </h1>
              <p className="text-gray-600 text-sm md:text-base">
                Define el nombre y los permisos del grupo
              </p>
            </div>
          </div>
        </div>

        {/* Form Container */}
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit}>
            <div className="bg-white rounded-2xl shadow-xl border border-green-100 overflow-hidden">
              {/* Form Header */}
              <div className="bg-gradient-to-r from-green-600 to-emerald-600 px-6 md:px-8 py-6">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 rounded-xl bg-green-500 flex items-center justify-center shadow-lg">
                    <Shield className="h-6 w-6 text-white" />
                  </div>
                  <h2 className="text-xl md:text-2xl font-bold text-white">
                    Información del Grupo
                  </h2>
                </div>
              </div>

              <div className="p-6 md:p-8">
                {/* Group Name */}
                <div className="mb-8">
                  <label htmlFor="group-name" className="block text-sm font-bold text-gray-700 mb-3">
                    Nombre del Grupo *
                  </label>
                  <input
                    type="text"
                    id="group-name"
                    name="groupName"
                    value={formData.name}
                    onChange={handleNameChange}
                    autoComplete="organization"
                    className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 focus:ring-green-200 focus:border-green-500 transition-all duration-300 ${
                      errors.name ? 'border-red-400' : 'border-gray-200'
                    }`}
                    placeholder="Ej: Administradores, Analistas, Visualizadores"
                  />
                  {errors.name && (
                    <p className="mt-2 text-sm text-red-600 font-medium">
                      {errors.name}
                    </p>
                  )}
                </div>

                {/* Permissions Section */}
                <div>
                  <div className="flex flex-col md:flex-row md:items-center justify-between mb-6">
                    <label htmlFor="permissions-search" className="block text-sm font-bold text-gray-700 mb-3 md:mb-0">
                      Permisos del Grupo
                    </label>
                    <div className="flex items-center space-x-4">
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={handleSelectAll}
                        className="text-sm"
                      >
                        {selectAll ? (
                          <>
                            <X size={16} className="mr-2" />
                            Deseleccionar todos
                          </>
                        ) : (
                          <>
                            <Check size={16} className="mr-2" />
                            Seleccionar todos
                          </>
                        )}
                      </Button>
                      <span className="text-sm text-gray-600 font-medium">
                        {formData.permissions.length} de {permissions.length} seleccionados
                      </span>
                    </div>
                  </div>

                  {/* Search Permissions */}
                  <div className="mb-6">
                    <input
                      type="text"
                      id="permissions-search"
                      name="permissionsSearch"
                      value={searchPermission}
                      onChange={(e) => setSearchPermission(e.target.value)}
                      autoComplete="off"
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-green-200 focus:border-green-500 transition-all duration-300"
                      placeholder="Buscar permisos..."
                    />
                  </div>

                  {/* Permissions List */}
                  {permissionsLoading ? (
                    <div className="flex items-center justify-center py-12">
                      <div className="animate-spin rounded-full h-8 w-8 border-4 border-green-600 border-t-transparent"></div>
                      <span className="ml-3 text-gray-600">Cargando permisos...</span>
                    </div>
                  ) : (
                    <div className="max-h-96 overflow-y-auto border-2 border-gray-200 rounded-xl p-4">
                      {Object.keys(groupedPermissions).length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                          No se encontraron permisos
                        </div>
                      ) : (
                        Object.entries(groupedPermissions).map(([model, modelPermissions]) => (
                          <div key={model} className="mb-6 last:mb-0">
                            <h4 className="text-sm font-bold text-gray-700 uppercase tracking-wider mb-3 flex items-center">
                              <Lock className="w-4 h-4 mr-2 text-green-600" />
                              {model}
                            </h4>
                            <div className="space-y-2">
                              {modelPermissions.map(permission => (
                                <label
                                  key={permission.id}
                                  htmlFor={`permission-${permission.id}`}
                                  className="flex items-center p-3 rounded-lg hover:bg-green-50 transition-colors duration-200 cursor-pointer"
                                >
                                  <input
                                    type="checkbox"
                                    id={`permission-${permission.id}`}
                                    name={`permission-${permission.id}`}
                                    className="w-5 h-5 text-green-600 border-2 border-gray-300 rounded focus:ring-green-500 focus:ring-3"
                                    checked={formData.permissions.includes(permission.id)}
                                    onChange={() => handlePermissionToggle(permission.id)}
                                  />
                                  <div className="ml-3 flex-1">
                                    <p className="text-sm font-medium text-gray-900">
                                      {permission.name}
                                    </p>
                                    <p className="text-xs text-gray-500">
                                      {permission.codename}
                                    </p>
                                  </div>
                                </label>
                              ))}
                            </div>
                          </div>
                        ))
                      )}
                    </div>
                  )}
                </div>
              </div>

              {/* Form Actions */}
              <div className="bg-gray-50 px-6 md:px-8 py-6 border-t border-gray-200">
                <div className="flex flex-col md:flex-row justify-end space-y-3 md:space-y-0 md:space-x-4">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleCancel}
                    disabled={loading}
                    className="w-full md:w-auto"
                  >
                    Cancelar
                  </Button>
                  <Button
                    type="submit"
                    variant="primary"
                    loading={loading}
                    disabled={loading || !formData.name.trim()}
                    className="w-full md:w-auto bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700"
                  >
                    Crear Grupo
                  </Button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CreateGroup;
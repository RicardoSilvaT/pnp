// src/pages/groups/ViewGroup.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Shield, Lock, Edit, Users, Check, X } from 'lucide-react';
import { useGroup, usePermissions } from '../../hooks/useGroups';
import Button from '../../Components/common/Button';

const ViewGroup = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { group, loading, error } = useGroup(id);
  const { permissions: allPermissions, loading: permissionsLoading } = usePermissions();
  const [enrichedPermissions, setEnrichedPermissions] = useState([]);

  const handleBack = () => {
    navigate('/groups');
  };

  const handleEdit = () => {
    navigate(`/groups/edit/${group.id}`);
  };

  // Enriquecer los permisos del grupo con sus detalles completos
  useEffect(() => {
    if (group && group.permissions && allPermissions.length > 0) {
      const enriched = group.permissions.map(permId => {
        // Si el permiso es un ID, buscar el objeto completo
        if (typeof permId === 'number') {
          return allPermissions.find(p => p.id === permId);
        }
        // Si ya es un objeto, devolverlo tal cual
        return permId;
      }).filter(Boolean); // Eliminar undefined/null

      setEnrichedPermissions(enriched);
    }
  }, [group, allPermissions]);

  // Agrupar permisos por modelo (igual que en EditGroup)
  const groupedPermissions = enrichedPermissions.reduce((acc, permission) => {
    if (!permission || !permission.codename) return acc;
    
    const parts = permission.codename.split('_') || [];
    const model = parts.length > 1 ? parts[parts.length - 1] : 'otros';
    
    if (!acc[model]) {
      acc[model] = [];
    }
    acc[model].push(permission);
    return acc;
  }, {});

  if (loading || permissionsLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-green-50 flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-green-700 border-t-transparent shadow-lg"></div>
          <p className="text-green-800 font-semibold text-lg">
            Cargando información del grupo...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-green-50 p-8">
        <div className="max-w-2xl mx-auto">
          <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6 shadow-lg">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold">!</span>
              </div>
              <div>
                <h3 className="text-red-800 font-semibold text-lg">
                  Error al cargar grupo
                </h3>
                <p className="text-red-600">{error}</p>
              </div>
            </div>
            <Button variant="outline" onClick={handleBack} className="mt-4">
              <ArrowLeft size={20} className="mr-2" />
              Volver a grupos
            </Button>
          </div>
        </div>
      </div>
    );
  }

  if (!group) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-green-50 p-8">
        <div className="max-w-2xl mx-auto">
          <div className="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-6 shadow-lg">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold">?</span>
              </div>
              <div>
                <h3 className="text-yellow-800 font-semibold text-lg">
                  Grupo no encontrado
                </h3>
                <p className="text-yellow-600">
                  El grupo solicitado no existe o no tienes permisos para verlo.
                </p>
              </div>
            </div>
            <Button variant="outline" onClick={handleBack} className="mt-4">
              <ArrowLeft size={20} className="mr-2" />
              Volver a grupos
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-green-50 to-emerald-50">
      <div className="max-w-6xl mx-auto px-4 md:px-6 py-8 md:py-12">
        {/* Header Section */}
        <section className="mb-8">
          <div className="flex items-center space-x-4">
            <Button
              variant="outline"
              onClick={handleBack}
              className="flex-shrink-0"
            >
              <ArrowLeft size={20} className="mr-2" />
              Volver
            </Button>
            <div>
              <h1 className="text-2xl md:text-3xl font-black bg-gradient-to-r from-green-700 via-green-600 to-amber-600 bg-clip-text text-transparent">
                Detalles del Grupo
              </h1>
              <p className="text-gray-600 text-sm md:text-base">
                Información completa del grupo y sus permisos
              </p>
            </div>
          </div>
        </section>

        {/* Group Profile Card */}
        <section className="mb-8">
          <div className="max-w-6xl mx-auto relative">
            {/* Edit Button */}
            <div className="flex justify-end mb-4">
              <Button
                variant="warning"
                onClick={handleEdit}
                className="shadow-lg"
              >
                <Edit size={20} className="mr-2" />
                Editar Grupo
              </Button>
            </div>

            <div className="bg-white rounded-2xl shadow-xl border border-green-100 overflow-hidden">
              {/* Profile Header */}
              <div className="bg-gradient-to-r from-green-600 to-emerald-600 px-6 md:px-8 py-8 md:py-12">
                <div className="flex flex-col md:flex-row items-center md:items-start space-y-4 md:space-y-0 md:space-x-8">
                  {/* Icon */}
                  <div className="flex-shrink-0">
                    <div className="w-24 h-24 md:w-32 md:h-32 rounded-2xl bg-green-500 flex items-center justify-center shadow-2xl">
                      <Shield className="h-12 w-12 md:h-16 md:w-16 text-white" />
                    </div>
                  </div>

                  {/* Group Info */}
                  <div className="flex-1 text-center md:text-left text-white">
                    <h2 className="text-2xl md:text-3xl font-black mb-3">
                      {group.name}
                    </h2>
                    <p className="text-lg md:text-xl text-green-100 font-medium mb-4">
                      ID: #{group.id}
                    </p>

                    {/* Stats */}
                    <div className="flex flex-wrap justify-center md:justify-start gap-4">
                      <div className="bg-green-500 bg-opacity-50 px-4 py-2 rounded-lg">
                        <div className="flex items-center space-x-2">
                          <Lock className="h-5 w-5" />
                          <span className="text-sm font-bold">
                            {enrichedPermissions.length} Permisos
                          </span>
                        </div>
                      </div>
                      <div className="bg-green-500 bg-opacity-50 px-4 py-2 rounded-lg">
                        <div className="flex items-center space-x-2">
                          <Users className="h-5 w-5" />
                          <span className="text-sm font-bold">
                            {group.user_count || 0} Usuarios
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Permissions Section */}
              <div className="p-6 md:p-8">
                <div className="max-w-5xl mx-auto">
                  <h3 className="text-xl font-bold text-gray-800 mb-6 flex items-center">
                    <Lock className="w-6 h-6 mr-2 text-green-600" />
                    Permisos Asignados
                  </h3>

                  {enrichedPermissions.length > 0 ? (
                    <div className="space-y-8">
                      {Object.entries(groupedPermissions).map(([model, permissions]) => (
                        <div key={model} className="bg-gray-50 rounded-xl p-6">
                          <h4 className="text-lg font-bold text-gray-700 mb-4 uppercase tracking-wider flex items-center">
                            <Shield className="w-5 h-5 mr-2 text-green-600" />
                            {model}
                          </h4>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {permissions.map((permission) => (
                              <div
                                key={permission.id}
                                className="bg-white rounded-lg p-4 shadow-sm border border-gray-200"
                              >
                                <div className="flex items-start space-x-3">
                                  <div className="flex-shrink-0 mt-1">
                                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                                      <Check className="w-4 h-4 text-green-600" />
                                    </div>
                                  </div>
                                  <div className="flex-1">
                                    <p className="text-sm font-semibold text-gray-900">
                                      {permission.name}
                                    </p>
                                    <p className="text-xs text-gray-500 mt-1">
                                      Código: {permission.codename}
                                    </p>
                                    <p className="text-xs text-gray-400 mt-1">
                                      ID: #{permission.id}
                                    </p>
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-12 bg-gray-50 rounded-xl">
                      <div className="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
                        <X className="h-10 w-10 text-gray-400" />
                      </div>
                      <h4 className="text-lg font-semibold text-gray-700 mb-2">
                        Sin Permisos Asignados
                      </h4>
                      <p className="text-gray-500">
                        Este grupo no tiene permisos asignados actualmente.
                      </p>
                      <Button
                        variant="primary"
                        onClick={handleEdit}
                        className="mt-4"
                      >
                        <Edit size={16} className="mr-2" />
                        Asignar Permisos
                      </Button>
                    </div>
                  )}
                </div>
              </div>

              {/* Summary Section */}
              <div className="bg-gray-50 p-6 md:p-8 border-t border-gray-200">
                <div className="max-w-5xl mx-auto">
                  <h3 className="text-lg font-bold text-gray-800 mb-4">
                    Resumen del Grupo
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                          <Shield className="w-6 h-6 text-green-600" />
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Nombre</p>
                          <p className="text-base font-semibold text-gray-900">
                            {group.name}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                          <Lock className="w-6 h-6 text-blue-600" />
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Total Permisos</p>
                          <p className="text-base font-semibold text-gray-900">
                            {enrichedPermissions.length}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
                          <Users className="w-6 h-6 text-amber-600" />
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Usuarios</p>
                          <p className="text-base font-semibold text-gray-900">
                            {group.user_count || 0}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default ViewGroup;
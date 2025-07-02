// src/pages/groups/GroupsPage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, Edit, Trash2, Eye, Shield, Lock, Users } from 'lucide-react';
import { useGroups } from '../../hooks/useGroups';
import Button from '../../Components/common/Button';

const GroupsPage = () => {
  const navigate = useNavigate();
  const { groups, loading, error, deleteGroup } = useGroups();
  const [searchTerm, setSearchTerm] = useState('');

  const filteredGroups = groups.filter(group =>
    group.name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDeleteGroup = async (id) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este grupo?')) {
      try {
        await deleteGroup(id);
        alert('Grupo eliminado exitosamente');
      } catch (error) {
        alert('Error al eliminar grupo: ' + error.message);
      }
    }
  };

  const handleCreateGroup = () => {
    navigate('/groups/create');
  };

  const handleEditGroup = (group) => {
    navigate(`/groups/edit/${group.id}`);
  };

  const handleViewGroup = (group) => {
    navigate(`/groups/view/${group.id}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-green-50 flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-green-700 border-t-transparent shadow-lg"></div>
          <p className="text-green-800 font-semibold text-lg">Cargando grupos...</p>
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
                <h3 className="text-red-800 font-semibold text-lg">Error al cargar grupos</h3>
                <p className="text-red-600">{error}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-green-50 to-emerald-50">
      <div className="max-w-7xl mx-auto px-4 md:px-6 py-8 md:py-12">
        
        {/* Header Section */}
        <section className="text-center mb-12 md:mb-20">
          <h1 className="text-3xl md:text-5xl font-black bg-gradient-to-r from-green-700 via-green-600 to-amber-600 bg-clip-text text-transparent mb-4 md:mb-6 tracking-tight px-4">
            Gestión de Grupos
          </h1>
          <div className="flex items-center justify-center">
            <div className="w-1 h-6 bg-gradient-to-b from-green-600 to-amber-500 rounded-full mr-4"></div>
            <p className="text-gray-700 text-base md:text-lg font-medium">
              Administra los grupos y permisos del sistema
            </p>
          </div>
        </section>

        {/* Search and Actions Section */}
        <section className="mb-12 md:mb-20">
          <div className="max-w-5xl mx-auto px-4">
            <div className="flex flex-col lg:flex-row justify-between items-center gap-6 md:gap-8">
              {/* Search Section */}
              <div className="w-full lg:flex-1 max-w-xl">
                <div className="relative">
                  <input
                    id="search-groups"
                    name="searchGroups"
                    type="text"
                    placeholder="Buscar grupos..."
                    className="w-full pl-4 md:pl-6 pr-4 md:pr-6 py-3 md:py-4 bg-white border-2 border-green-200 rounded-xl focus:ring-4 focus:ring-green-200 focus:border-green-500 transition-all duration-300 shadow-md hover:shadow-lg text-gray-700 placeholder-gray-500 text-sm md:text-base"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>

              {/* Add Group Button */}
              <div className="w-full lg:w-auto">
                <Button
                  variant="success"
                  size="lg"
                  onClick={handleCreateGroup}
                  className="w-full lg:w-auto bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white px-6 md:px-8 py-3 md:py-4 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 font-semibold text-base md:text-lg"
                >
                  <Plus size={20} className="mr-2 md:mr-3" />
                  Nuevo Grupo
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Stats Cards Section */}
        <section className="mb-20 md:mb-32">
          <div className="max-w-5xl mx-auto px-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-16">
              <div className="group bg-gradient-to-br from-white to-green-50 p-6 md:p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 border border-green-100 hover:border-green-300 transform hover:-translate-y-2">
                <div className="text-center">
                  <div className="w-16 h-16 md:w-18 md:h-18 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300 mx-auto mb-4 md:mb-5">
                    <Shield className="h-8 w-8 md:h-9 md:w-9 text-white" />
                  </div>
                  <p className="text-green-700 font-bold text-base md:text-lg uppercase tracking-wide mb-3 md:mb-4">Total Grupos</p>
                  <p className="text-4xl md:text-6xl font-black text-green-800">{groups.length}</p>
                </div>
              </div>

              <div className="group bg-gradient-to-br from-white to-emerald-50 p-6 md:p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 border border-emerald-100 hover:border-emerald-300 transform hover:-translate-y-2">
                <div className="text-center">
                  <div className="w-16 h-16 md:w-18 md:h-18 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300 mx-auto mb-4 md:mb-5">
                    <Lock className="h-8 w-8 md:h-9 md:w-9 text-white" />
                  </div>
                  <p className="text-emerald-700 font-bold text-base md:text-lg uppercase tracking-wide mb-3 md:mb-4">Permisos Totales</p>
                  <p className="text-4xl md:text-6xl font-black text-emerald-800">
                    {groups.reduce((acc, group) => acc + (group.permissions?.length || 0), 0)}
                  </p>
                </div>
              </div>

              <div className="group bg-gradient-to-br from-white to-amber-50 p-6 md:p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 border border-amber-100 hover:border-amber-300 transform hover:-translate-y-2 sm:col-span-2 lg:col-span-1">
                <div className="text-center">
                  <div className="w-16 h-16 md:w-18 md:h-18 bg-gradient-to-br from-amber-500 to-amber-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300 mx-auto mb-4 md:mb-5">
                    <Users className="h-8 w-8 md:h-9 md:w-9 text-white" />
                  </div>
                  <p className="text-amber-700 font-bold text-base md:text-lg uppercase tracking-wide mb-3 md:mb-4">Grupos Activos</p>
                  <p className="text-4xl md:text-6xl font-black text-amber-800">
                    {groups.filter(group => group.permissions?.length > 0).length}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Groups Table Section */}
        <section>
          <div className="max-w-5xl mx-auto px-4 flex justify-center">
            {/* Desktop Table View */}
            <div className="hidden lg:block bg-white rounded-2xl shadow-xl border border-green-100 overflow-hidden w-full">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gradient-to-r from-green-600 to-emerald-600">
                    <tr>
                      <th className="w-1/3 px-8 py-6 text-center text-base font-bold text-white uppercase tracking-wider">
                        Nombre del Grupo
                      </th>
                      <th className="w-1/3 px-8 py-6 text-center text-base font-bold text-white uppercase tracking-wider">
                        Cantidad de Permisos
                      </th>
                      <th className="w-1/3 px-8 py-6 text-center text-base font-bold text-white uppercase tracking-wider">
                        Acciones
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-green-100">
                    {filteredGroups.map((group, index) => (
                      <tr 
                        key={group.id} 
                        className="hover:bg-gradient-to-r hover:from-green-50 hover:to-emerald-50 transition-all duration-300 hover:shadow-lg group"
                      >
                        <td className="px-8 py-8">
                          <div className="flex items-center space-x-4">
                            <div className="flex-shrink-0">
                              <div className="h-14 w-14 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
                                <Shield className="h-8 w-8 text-white" />
                              </div>
                            </div>
                            <div className="min-w-0 flex-1">
                              <div className="text-lg font-bold text-gray-900 truncate">
                                {group.name}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="px-8 py-8 text-center">
                          <span className="inline-flex items-center px-4 py-2 text-base font-bold rounded-full shadow-md bg-gradient-to-r from-blue-500 to-blue-600 text-white">
                            <Lock className="h-4 w-4 mr-2" />
                            {group.permissions?.length || 0} permisos
                          </span>
                        </td>
                        <td className="px-8 py-8">
                          <div className="flex justify-center space-x-3">
                            <button 
                              className="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-110 flex items-center justify-center"
                              onClick={() => handleViewGroup(group)}
                              title="Ver detalles"
                            >
                              <Eye size={18} />
                            </button>
                            <button 
                              className="w-12 h-12 bg-gradient-to-r from-amber-500 to-amber-600 text-white rounded-lg hover:from-amber-600 hover:to-amber-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-110 flex items-center justify-center"
                              onClick={() => handleEditGroup(group)}
                              title="Editar grupo"
                            >
                              <Edit size={18} />
                            </button>
                            <button 
                              className="w-12 h-12 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg hover:from-red-600 hover:to-red-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-110 flex items-center justify-center"
                              onClick={() => handleDeleteGroup(group.id)}
                              title="Eliminar grupo"
                            >
                              <Trash2 size={18} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                {filteredGroups.length === 0 && (
                  <div className="text-center py-20">
                    <div className="w-24 h-24 bg-gradient-to-br from-green-200 to-green-300 rounded-full flex items-center justify-center mx-auto mb-8">
                      <Shield className="h-12 w-12 text-green-600" />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-700 mb-3">No se encontraron grupos</h3>
                    <p className="text-lg text-gray-500">Intenta con diferentes términos de búsqueda</p>
                  </div>
                )}
              </div>
            </div>

            {/* Mobile Card View */}
            <div className="lg:hidden space-y-6">
              {filteredGroups.map((group) => (
                <div 
                  key={group.id}
                  className="bg-white rounded-xl shadow-lg border border-green-100 p-6 hover:shadow-xl transition-shadow duration-300"
                >
                  {/* Header - Group Info */}
                  <div className="flex items-center space-x-4 mb-5">
                    <div className="h-16 w-16 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-lg">
                      <Shield className="h-8 w-8 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-xl font-bold text-gray-900 truncate">
                        {group.name}
                      </h3>
                    </div>
                  </div>

                  {/* Group Info */}
                  <div className="space-y-4 mb-5">
                    <div className="flex justify-between items-center">
                      <span className="text-base font-medium text-gray-500">Permisos:</span>
                      <span className="inline-flex items-center px-3 py-1 text-sm font-bold rounded-full shadow-md bg-gradient-to-r from-blue-500 to-blue-600 text-white">
                        <Lock className="h-3 w-3 mr-1" />
                        {group.permissions?.length || 0}
                      </span>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex justify-end space-x-3 pt-4 border-t border-gray-100">
                    <button 
                      className="flex items-center justify-center px-5 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 text-base font-medium"
                      onClick={() => handleViewGroup(group)}
                    >
                      <Eye size={18} className="mr-2" />
                      Ver
                    </button>
                    <button 
                      className="flex items-center justify-center px-5 py-3 bg-gradient-to-r from-amber-500 to-amber-600 text-white rounded-lg hover:from-amber-600 hover:to-amber-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 text-base font-medium"
                      onClick={() => handleEditGroup(group)}
                    >
                      <Edit size={18} className="mr-2" />
                      Editar
                    </button>
                    <button 
                      className="flex items-center justify-center px-5 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg hover:from-red-600 hover:to-red-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 text-base font-medium"
                      onClick={() => handleDeleteGroup(group.id)}
                    >
                      <Trash2 size={18} className="mr-2" />
                      Eliminar
                    </button>
                  </div>
                </div>
              ))}

              {filteredGroups.length === 0 && (
                <div className="text-center py-16">
                  <div className="w-20 h-20 bg-gradient-to-br from-green-200 to-green-300 rounded-full flex items-center justify-center mx-auto mb-6">
                    <Shield className="h-10 w-10 text-green-600" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-700 mb-3">No se encontraron grupos</h3>
                  <p className="text-base text-gray-500">Intenta con diferentes términos de búsqueda</p>
                </div>
              )}
            </div>
          </div>
        </section>

      </div>
    </div>
  );
};

export default GroupsPage;
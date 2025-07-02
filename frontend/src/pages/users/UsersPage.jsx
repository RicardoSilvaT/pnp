import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, Edit, Trash2, Eye, Users, Shield, UserCheck } from 'lucide-react';
import { useUsers } from '../../hooks/useUsers';
import Button from '../../Components/common/Button';

const UsersPage = () => {
  const navigate = useNavigate();
  const { users, loading, error, deleteUser } = useUsers();
  const [searchTerm, setSearchTerm] = useState('');

  const filteredUsers = users.filter(user =>
    user.username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.first_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.last_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.dni?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.phone?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDeleteUser = async (id) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
      try {
        await deleteUser(id);
        alert('Usuario eliminado exitosamente');
      } catch (error) {
        alert('Error al eliminar usuario: ' + error.message);
      }
    }
  };

  // CORREGIDO: Rutas sin /app/ prefix porque ya no lo necesitamos
  const handleCreateUser = () => {
    navigate('/users/create');
  };

  const handleEditUser = (user) => {
    navigate(`/users/edit/${user.id}`);
  };

  const handleViewUser = (user) => {
    navigate(`/users/view/${user.id}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-green-50 flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-green-700 border-t-transparent shadow-lg"></div>
          <p className="text-green-800 font-semibold text-lg">Cargando usuarios...</p>
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
                <h3 className="text-red-800 font-semibold text-lg">Error al cargar usuarios</h3>
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
      <div className="max-w-full xl:max-w-7xl mx-auto px-4 md:px-6 py-6 md:py-8">
        
        {/* Header Section */}
        <section className="text-center mb-6 md:mb-10">
          <h1 className="text-3xl md:text-5xl font-black bg-gradient-to-r from-green-700 via-green-600 to-amber-600 bg-clip-text text-transparent mb-4 md:mb-6 tracking-tight px-4">
            Gestión de Usuarios
          </h1>
          <div className="flex items-center justify-center">
            <div className="w-1 h-6 bg-gradient-to-b from-green-600 to-amber-500 rounded-full mr-4"></div>
            <p className="text-gray-700 text-base md:text-lg font-medium">
              Administra los usuarios del sistema
            </p>
          </div>
        </section>

        {/* Search and Actions Section*/}
        <section className="mb-5 md:mb-5">
          <div className="max-w-5xl mx-auto px-4">
            <div className="flex flex-col lg:flex-row justify-between items-center gap-6 md:gap-8">
              {/* Search Section */}
              <div className="w-full lg:flex-1 max-w-xl">
                <div className="relative">
                  <input
                    id="search-users"
                    name="searchUsers"
                    type="text"
                    placeholder="Buscar usuarios..."
                    className="w-full pl-4 md:pl-6 pr-4 md:pr-6 py-3 md:py-4 bg-white border-2 border-green-200 rounded-xl focus:ring-4 focus:ring-green-200 focus:border-green-500 transition-all duration-300 shadow-md hover:shadow-lg text-gray-700 placeholder-gray-500 text-sm md:text-base"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>

              {/* Add User Button */}
              <div className="w-full lg:w-auto">
                <Button
                  variant="success"
                  size="lg"
                  onClick={handleCreateUser}
                  className="w-full lg:w-auto bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white px-6 md:px-8 py-3 md:py-4 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 font-semibold text-base md:text-lg"
                >
                  <Plus size={20} className="mr-2 md:mr-3" />
                  Nuevo Usuario
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Stats Cards Section */}
        <section className="mb-8 md:mb-8">
          <div className="max-w-5xl mx-auto px-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 md:gap-8 justify-items-center">
              <div className="group bg-gradient-to-br from-white to-green-50 p-6 md:p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 border border-green-100 hover:border-green-300 transform hover:-translate-y-2">
                <div className="text-center">
                  <div className="w-16 h-16 md:w-18 md:h-18 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300 mx-auto mb-4 md:mb-5">
                    <Users className="h-8 w-8 md:h-9 md:w-9 text-white" />
                  </div>
                  <p className="text-green-700 font-bold text-base md:text-lg uppercase tracking-wide mb-3 md:mb-4">Total Usuarios</p>
                  <p className="text-4xl md:text-6xl font-black text-green-800">{users.length}</p>
                </div>
              </div>

              <div className="group bg-gradient-to-br from-white to-emerald-50 p-6 md:p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 border border-emerald-100 hover:border-emerald-300 transform hover:-translate-y-2">
                <div className="text-center">
                  <div className="w-16 h-16 md:w-18 md:h-18 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300 mx-auto mb-4 md:mb-5">
                    <UserCheck className="h-8 w-8 md:h-9 md:w-9 text-white" />
                  </div>
                  <p className="text-emerald-700 font-bold text-base md:text-lg uppercase tracking-wide mb-3 md:mb-4">Usuarios Activos</p>
                  <p className="text-4xl md:text-6xl font-black text-emerald-800">
                    {users.filter(user => user.is_active).length}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Users Table Section */}
        <section>
          <div className="max-w-full mx-auto px-4">
            {/* Desktop Table View - TABLA MEJORADA */}
            <div className="hidden lg:block bg-white rounded-2xl shadow-xl border border-green-100 overflow-hidden w-full">
              <table className="w-full table-fixed">
                <thead className="bg-gradient-to-r from-green-600 to-emerald-600">
                  <tr>
                    <th className="w-64 px-4 py-4 text-center text-sm font-bold text-white uppercase tracking-wider">
                      Usuario
                    </th>
                    <th className="w-48 px-4 py-4 text-center text-sm font-bold text-white uppercase tracking-wider">
                      Email
                    </th>
                    <th className="w-24 px-4 py-4 text-center text-sm font-bold text-white uppercase tracking-wider">
                      DNI
                    </th>
                    <th className="w-32 px-4 py-4 text-center text-sm font-bold text-white uppercase tracking-wider">
                      Teléfono
                    </th>
                    <th className="w-28 px-4 py-4 text-center text-sm font-bold text-white uppercase tracking-wider">
                      Grupo
                    </th>
                    <th className="w-32 px-4 py-4 text-center text-sm font-bold text-white uppercase tracking-wider">
                      Estado
                    </th>
                    <th className="w-36 px-4 py-4 text-center text-sm font-bold text-white uppercase tracking-wider">
                      Acciones
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-green-100">
                  {filteredUsers.map((user, index) => (
                    <tr 
                      key={user.id} 
                      className="hover:bg-gradient-to-r hover:from-green-50 hover:to-emerald-50 transition-all duration-300 hover:shadow-lg group"
                    >
                      <td className="px-4 py-4">
                        <div className="flex items-center space-x-3">
                          <div className="flex-shrink-0">
                            <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-md">
                              <span className="text-white font-bold text-sm">
                                {user.first_name?.[0] || user.username?.[0] || 'U'}
                              </span>
                            </div>
                          </div>
                          <div className="min-w-0 flex-1">
                            <div className="text-sm font-bold text-gray-900 truncate">
                              {user.first_name} {user.last_name}
                            </div>
                            <div className="text-xs text-green-600 font-medium truncate">
                              @{user.username}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-4 text-center">
                        <div className="text-sm font-medium text-gray-900 truncate" title={user.email}>
                          {user.email}
                        </div>
                      </td>
                      <td className="px-4 py-4 text-center">
                        <div className="text-sm font-medium text-gray-900">{user.dni}</div>
                      </td>
                      <td className="px-4 py-4 text-center">
                        <div className="text-sm font-medium text-gray-900">{user.phone || '-'}</div>
                      </td>
                      <td className="px-4 py-4 text-center">
                        <span className={`inline-flex px-2 py-1 text-xs font-bold rounded-full shadow-sm ${
                          user.group_name || user.groups?.[0] 
                            ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white' 
                            : 'bg-gradient-to-r from-gray-400 to-gray-500 text-white'
                        }`} title={user.group_name || user.groups?.[0] || 'Sin grupo'}>
                          {user.group_name || user.groups?.[0] || 'Sin grupo'}
                        </span>
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex flex-col items-center space-y-1">
                          <span className={`inline-flex px-2 py-1 text-xs font-bold rounded-full shadow-sm ${
                            user.is_active 
                              ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white' 
                              : 'bg-gradient-to-r from-red-500 to-red-600 text-white'
                          }`}>
                            {user.is_active ? 'Activo' : 'Inactivo'}
                          </span>
                          {user.is_staff && (
                            <span className="bg-gradient-to-r from-amber-500 to-amber-600 text-white px-2 py-1 text-xs font-bold rounded-full shadow-sm">
                              Staff
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex justify-center space-x-2">
                          <button 
                            className="w-8 h-8 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-md hover:from-blue-600 hover:to-blue-700 transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-110 flex items-center justify-center"
                            onClick={() => handleViewUser(user)}
                            title="Ver detalles"
                          >
                            <Eye size={14} />
                          </button>
                          <button 
                            className="w-8 h-8 bg-gradient-to-r from-amber-500 to-amber-600 text-white rounded-md hover:from-amber-600 hover:to-amber-700 transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-110 flex items-center justify-center"
                            onClick={() => handleEditUser(user)}
                            title="Editar usuario"
                          >
                            <Edit size={14} />
                          </button>
                          <button 
                            className="w-8 h-8 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-md hover:from-red-600 hover:to-red-700 transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-110 flex items-center justify-center"
                            onClick={() => handleDeleteUser(user.id)}
                            title="Eliminar usuario"
                          >
                            <Trash2 size={14} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {filteredUsers.length === 0 && (
                <div className="text-center py-16">
                  <div className="w-20 h-20 bg-gradient-to-br from-green-200 to-green-300 rounded-full flex items-center justify-center mx-auto mb-6">
                    <Users className="h-10 w-10 text-green-600" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-700 mb-3">No se encontraron usuarios</h3>
                  <p className="text-base text-gray-500">Intenta con diferentes términos de búsqueda</p>
                </div>
              )}
            </div>

            {/* Mobile Card View */}
            <div className="lg:hidden space-y-4">
              {filteredUsers.map((user) => (
                <div 
                  key={user.id}
                  className="bg-white rounded-xl shadow-lg border border-green-100 p-4 hover:shadow-xl transition-shadow duration-300"
                >
                  {/* Header - User Info */}
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="h-12 w-12 rounded-lg bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-lg">
                      <span className="text-white font-bold text-lg">
                        {user.first_name?.[0] || user.username?.[0] || 'U'}
                      </span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg font-bold text-gray-900 truncate">
                        {user.first_name} {user.last_name}
                      </h3>
                      <p className="text-sm text-green-600 font-medium truncate">
                        @{user.username}
                      </p>
                    </div>
                  </div>

                  {/* Contact Info */}
                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium text-gray-500">Email:</span>
                      <span className="text-sm text-gray-900 truncate max-w-48">{user.email}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium text-gray-500">DNI:</span>
                      <span className="text-sm text-gray-900">{user.dni}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium text-gray-500">Teléfono:</span>
                      <span className="text-sm text-gray-900">{user.phone || '-'}</span>
                    </div>
                  </div>

                  {/* Status and Role */}
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className={`inline-flex px-3 py-1 text-sm font-bold rounded-full shadow-md ${
                      user.is_active 
                        ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white' 
                        : 'bg-gradient-to-r from-red-500 to-red-600 text-white'
                    }`}>
                      {user.is_active ? 'Activo' : 'Inactivo'}
                    </span>
                    
                    <span className={`inline-flex px-3 py-1 text-sm font-bold rounded-full shadow-md ${
                      user.group_name || user.groups?.[0] 
                        ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white' 
                        : 'bg-gradient-to-r from-gray-400 to-gray-500 text-white'
                    }`}>
                      {user.group_name || user.groups?.[0] || 'Sin grupo'}
                    </span>

                    {user.is_staff && (
                      <span className="bg-gradient-to-r from-amber-500 to-amber-600 text-white px-3 py-1 text-sm font-bold rounded-full shadow-md">
                        Staff
                      </span>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex justify-end space-x-2 pt-3 border-t border-gray-100">
                    <button 
                      className="flex items-center justify-center px-3 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 text-sm font-medium"
                      onClick={() => handleViewUser(user)}
                    >
                      <Eye size={16} className="mr-1" />
                      Ver
                    </button>
                    <button 
                      className="flex items-center justify-center px-3 py-2 bg-gradient-to-r from-amber-500 to-amber-600 text-white rounded-lg hover:from-amber-600 hover:to-amber-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 text-sm font-medium"
                      onClick={() => handleEditUser(user)}
                    >
                      <Edit size={16} className="mr-1" />
                      Editar
                    </button>
                    <button 
                      className="flex items-center justify-center px-3 py-2 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg hover:from-red-600 hover:to-red-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 text-sm font-medium"
                      onClick={() => handleDeleteUser(user.id)}
                    >
                      <Trash2 size={16} className="mr-1" />
                      Eliminar
                    </button>
                  </div>
                </div>
              ))}

              {filteredUsers.length === 0 && (
                <div className="text-center py-12">
                  <div className="w-16 h-16 bg-gradient-to-br from-green-200 to-green-300 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Users className="h-8 w-8 text-green-600" />
                  </div>
                  <h3 className="text-lg font-bold text-gray-700 mb-2">No se encontraron usuarios</h3>
                  <p className="text-sm text-gray-500">Intenta con diferentes términos de búsqueda</p>
                </div>
              )}
            </div>
          </div>
        </section>

      </div>
    </div>
  );
};

export default UsersPage;
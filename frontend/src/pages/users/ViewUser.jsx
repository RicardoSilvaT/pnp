import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  ArrowLeft,
  User,
  Mail,
  Phone,
  IdCard,
  Calendar,
  Shield,
  UserCheck,
  Settings,
  Clock,
  Edit,
  Loader,
  Users,
} from "lucide-react";
import { useUser } from "../../hooks/useUsers";
import {
  formatFullName,
  getUserInitials,
  formatDate,
} from "../../utils/userConstants";
import Button from "../../Components/common/Button";

// Función auxiliar para obtener el grupo del usuario
const getUserGroup = (user) => {
  // Priorizar group_frontend, luego group_name, luego groups array
  if (user.group_frontend) {
    return user.group_frontend;
  }
  
  if (user.group_name) {
    return user.group_name;
  }
  
  if (user.groups && Array.isArray(user.groups) && user.groups.length > 0) {
    // Si groups es un array de objetos con name
    if (user.groups[0].name) {
      return user.groups[0].name;
    }
    // Si groups es un array de strings
    return user.groups[0];
  }
  
  return null;
};

// Función auxiliar para formatear el nombre del grupo
const formatGroupName = (groupName) => {
  if (!groupName) return null;
  
  const groupMap = {
    'analista': 'Analista',
    'administrador': 'Administrador',
    'visualizador': 'Visualizador'
  };
  
  const lowerGroupName = groupName.toLowerCase();
  return groupMap[lowerGroupName] || groupName.charAt(0).toUpperCase() + groupName.slice(1);
};

const ViewUser = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { user, loading, error } = useUser(id);

  const handleBack = () => {
    navigate("/users");
  };

  const handleEdit = () => {
    navigate(`/users/edit/${user.id}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-green-50 flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-green-700 border-t-transparent shadow-lg"></div>
          <p className="text-green-800 font-semibold text-lg">
            Cargando información del usuario...
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
                  Error al cargar usuario
                </h3>
                <p className="text-red-600">{error}</p>
              </div>
            </div>
            <Button variant="outline" onClick={handleBack} className="mt-4">
              <ArrowLeft size={20} className="mr-2" />
              Volver a usuarios
            </Button>
          </div>
        </div>
      </div>
    );
  }

  if (!user) {
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
                  Usuario no encontrado
                </h3>
                <p className="text-yellow-600">
                  El usuario solicitado no existe o no tienes permisos para
                  verlo.
                </p>
              </div>
            </div>
            <Button variant="outline" onClick={handleBack} className="mt-4">
              <ArrowLeft size={20} className="mr-2" />
              Volver a usuarios
            </Button>
          </div>
        </div>
      </div>
    );
  }

  // Obtener el grupo del usuario
  const userGroup = getUserGroup(user);
  const formattedGroupName = formatGroupName(userGroup);

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
                Perfil de Usuario
              </h1>
              <p className="text-gray-600 text-sm md:text-base">
                Información detallada del usuario
              </p>
            </div>
          </div>
        </section>

        {/* User Profile Card */}
        <section className="mb-8">
          <div className="max-w-6xl mx-auto relative" />
          {/* Edit Button positioned absolutely */}
          <div className="flex justify-end mb-4">
            <Button
              variant="warning"
              onClick={handleEdit}
              className="shadow-lg"
            >
              <Edit size={20} className="mr-2" />
              Editar Usuario
            </Button>
          </div>

          <div className="bg-white rounded-2xl shadow-xl border border-green-100 overflow-hidden">
            {/* Profile Header */}
            <div className="bg-gradient-to-r from-green-600 to-emerald-600 px-6 md:px-8 py-8 md:py-12">
              <div className="flex flex-col md:flex-row items-center md:items-start space-y-4 md:space-y-0 md:space-x-8">
                {/* Avatar */}
                <div className="flex-shrink-0">
                  <div className="w-24 h-24 md:w-32 md:h-32 rounded-2xl bg-green-500 flex items-center justify-center shadow-2xl">
                    <span className="text-white font-black text-3xl md:text-4xl">
                      {getUserInitials(user)}
                    </span>
                  </div>
                </div>

                {/* User Info */}
                <div className="flex-1 text-center md:text-left text-white">
                  <h2 className="text-2xl md:text-3xl font-black mb-3 md:ml-4">
                    {formatFullName(user)}
                  </h2>
                  <p className="text-lg md:text-xl text-green-100 font-medium mb-2 md:ml-4">
                    @{user.username}
                  </p>
                  <p className="text-base md:text-lg text-green-200 mb-4 md:ml-4">
                    {user.email}
                  </p>

                  {/* Status Badges */}
                  <div className="flex flex-wrap justify-center md:justify-start md:ml-4 gap-2">
                    <span
                      className={`inline-flex px-4 py-2 text-sm font-bold rounded-full shadow-md ${
                        user.is_active
                          ? "bg-green-500 text-white"
                          : "bg-red-500 text-white"
                      }`}
                    >
                      {user.is_active ? "Activo" : "Inactivo"}
                    </span>

                    {user.is_staff && (
                      <span className="bg-amber-500 text-white px-4 py-2 text-sm font-bold rounded-full shadow-md">
                        Staff
                      </span>
                    )}

                    {formattedGroupName && (
                      <span className="bg-purple-500 text-white px-4 py-2 text-sm font-bold rounded-full shadow-md">
                        {formattedGroupName}
                      </span>
                    )}

                    {user.role && (
                      <span className="bg-blue-500 text-white px-4 py-2 text-sm font-bold rounded-full shadow-md">
                        {user.role.name}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* User Details */}
            <div className="p-6 md:p-8">
              <div className="max-w-5xl mx-auto">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
                  {/* Personal Information */}
                  <div className="space-y-6">
                    <h3 className="text-lg font-bold text-gray-800 flex items-center">
                      <User className="w-5 h-5 mr-2 text-green-600" />
                      Información Personal
                    </h3>

                    <div className="space-y-4">
                      <div className="flex items-start space-x-3">
                        <IdCard className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-sm text-gray-500 font-medium">
                            DNI
                          </p>
                          <p className="text-base font-semibold text-gray-900">
                            {user.dni || 'No especificado'}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-start space-x-3">
                        <Mail className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-sm text-gray-500 font-medium">
                            Email
                          </p>
                          <p className="text-base font-semibold text-gray-900 break-all">
                            {user.email}
                          </p>
                        </div>
                      </div>

                      {user.phone ? (
                        <div className="flex items-start space-x-3">
                          <Phone className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
                          <div>
                            <p className="text-sm text-gray-500 font-medium">
                              Teléfono
                            </p>
                            <p className="text-base font-semibold text-gray-900">
                              {user.phone}
                            </p>
                          </div>
                        </div>
                      ) : (
                        <div className="flex items-start space-x-3">
                          <Phone className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
                          <div>
                            <p className="text-sm text-gray-500 font-medium">
                              Teléfono
                            </p>
                            <p className="text-base font-semibold text-gray-400 italic">
                              No especificado
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Account Information */}
                  <div className="space-y-6">
                    <h3 className="text-lg font-bold text-gray-800 flex items-center">
                      <Settings className="w-5 h-5 mr-2 text-green-600" />
                      Información de Cuenta
                    </h3>

                    <div className="space-y-4">
                      <div className="flex items-start space-x-3">
                        <UserCheck className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-sm text-gray-500 font-medium">
                            Estado
                          </p>
                          <p
                            className={`text-base font-semibold ${
                              user.is_active ? "text-green-600" : "text-red-600"
                            }`}
                          >
                            {user.is_active
                              ? "Cuenta Activa"
                              : "Cuenta Inactiva"}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-start space-x-3">
                        <Shield className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-sm text-gray-500 font-medium">
                            Permisos
                          </p>
                          <p
                            className={`text-base font-semibold ${
                              user.is_staff ? "text-amber-600" : "text-gray-600"
                            }`}
                          >
                            {user.is_staff
                              ? "Personal de Staff"
                              : "Usuario Regular"}
                          </p>
                        </div>
                      </div>

                      {/* Grupo del usuario */}
                      <div className="flex items-start space-x-3">
                        <Users className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-sm text-gray-500 font-medium">
                            Grupo
                          </p>
                          {formattedGroupName ? (
                            <p className="text-base font-semibold text-purple-600">
                              {formattedGroupName}
                            </p>
                          ) : (
                            <p className="text-base font-semibold text-gray-400 italic">
                              Sin grupo asignado
                            </p>
                          )}
                        </div>
                      </div>

                      {user.role && (
                        <div className="flex items-start space-x-3">
                          <Settings className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
                          <div>
                            <p className="text-sm text-gray-500 font-medium">
                              Rol
                            </p>
                            <p className="text-base font-semibold text-blue-600">
                              {user.role.name}
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Activity Information */}
                  <div className="space-y-6">
                    <h3 className="text-lg font-bold text-gray-800 flex items-center">
                      <Clock className="w-5 h-5 mr-2 text-green-600" />
                      Actividad
                    </h3>

                    <div className="space-y-4">
                      <div className="flex items-start space-x-3">
                        <Calendar className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-sm text-gray-500 font-medium">
                            Fecha de Registro
                          </p>
                          <p className="text-base font-semibold text-gray-900">
                            {formatDate(user.created_at)}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-start space-x-3">
                        <Clock className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-sm text-gray-500 font-medium">
                            Último Acceso
                          </p>
                          <p className="text-base font-semibold text-gray-900">
                            {user.last_login
                              ? formatDate(user.last_login)
                              : "Nunca"}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-start space-x-3">
                        <User className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-sm text-gray-500 font-medium">
                            ID de Usuario
                          </p>
                          <p className="text-base font-semibold text-gray-900">
                            #{user.id}
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

        {/* Additional Group Information - Solo mostrar si hay grupos adicionales */}
        {user.groups && Array.isArray(user.groups) && user.groups.length > 1 && (
          <section className="mb-8">
            <div className="max-w-6xl mx-auto">
              <div className="bg-white rounded-2xl shadow-xl border border-green-100 p-6 md:p-8">
                <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
                  <Shield className="w-5 h-5 mr-2 text-green-600" />
                  Grupos Adicionales
                </h3>

                <div className="flex flex-wrap gap-2">
                  {user.groups.slice(1).map((group, index) => (
                    <span
                      key={index}
                      className="bg-gradient-to-r from-purple-500 to-purple-600 text-white px-4 py-2 text-sm font-bold rounded-full shadow-md"
                    >
                      {group.name || group}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}
      </div>
    </div>
  );
};

export default ViewUser;
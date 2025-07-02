import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import userService from '../services/userService';
import { formatFullName } from '../utils/userConstants';

// Hook para el usuario actual
const useCurrentUser = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchCurrentUser = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        const tokenPayload = JSON.parse(atob(token.split('.')[1]));
        const userId = tokenPayload.user_id;
        const data = await userService.getUserById(userId);
        setCurrentUser(data);
      }
    } catch (err) {
      console.error('Error obteniendo usuario actual:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCurrentUser();
  }, []);

  return { currentUser, loading };
};

const UserDashboard = () => {
  const navigate = useNavigate();
  const { currentUser, loading } = useCurrentUser();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login', { replace: true });
  };

  const getDisplayName = () => {
    if (!currentUser) return 'Usuario';
    const fullName = formatFullName(currentUser);
    return fullName && fullName !== currentUser.username ? fullName : currentUser.username || 'Usuario';
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-blue-50 p-4 font-sans">
      <h1 className="text-5xl font-extrabold text-blue-800 mb-6 text-center animate-pulse">
        {loading ? (
          '¡Bienvenido!'
        ) : (
          `¡Bienvenido, ${getDisplayName()}!`
        )}
      </h1>
      <p className="text-xl text-gray-700 mb-8 text-center max-w-lg">
        Has iniciado sesión con éxito.
      </p>
      <button
        onClick={handleLogout}
        className="px-8 py-4 bg-red-600 text-white font-semibold rounded-lg shadow-lg hover:bg-red-700 focus:outline-none focus:ring-4 focus:ring-red-400 focus:ring-offset-2 transition-all duration-300 transform hover:scale-105"
      >
        Cerrar Sesión
      </button>
    </div>
  );
};

export default UserDashboard;
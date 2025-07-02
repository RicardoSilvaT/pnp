import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faLock, faEye, faEyeSlash, faTimes } from '@fortawesome/free-solid-svg-icons';
import { useAuthContext } from '../contexts/AuthContext';

import policiaLoginImage from '../assets/images/logo_policia.jpg';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showNotification, setShowNotification] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const navigate = useNavigate();
  
  // Usar el contexto de autenticación
  const { login } = useAuthContext();

  const SESSION_TIMEOUT_SECONDS = 300; // 2 minutos

  const setupSessionTimeout = () => {
    if (!rememberMe) {
      const timeoutMs = SESSION_TIMEOUT_SECONDS * 1000;
      const expirationTime = Date.now() + timeoutMs;
      
      localStorage.setItem('session_expiration', expirationTime.toString());
      
      const timeoutId = setTimeout(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('session_expiration');
        
        alert('Tu sesión ha expirado por límite de tiempo. Por favor, inicia sesión nuevamente.');
        
        navigate('/');
      }, timeoutMs);
      
      localStorage.setItem('session_timeout_id', timeoutId.toString());
    } else {
      localStorage.removeItem('session_expiration');
      localStorage.removeItem('session_timeout_id');
    }
  };

  const checkSessionExpiration = () => {
    const expirationTime = localStorage.getItem('session_expiration');
    if (expirationTime && Date.now() > parseInt(expirationTime)) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('session_expiration');
      localStorage.removeItem('session_timeout_id');
      return true;
    }
    return false;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await login(username, password);
      if (result.success) {
        setupSessionTimeout();
        
        // Pequeño delay para asegurar que el estado se actualice
        setTimeout(() => {
          navigate('/dashboard');
        }, 100);
      } else {
        setError(result.error || 'Usuario o contraseña inválidos');
      }
    } catch (err) {
      setError('Error al conectar con el servidor');
    } finally {
      setLoading(false);
    }
  };

  const handleHelpClick = (e) => {
    e.preventDefault();
    setShowNotification(true);
    
    setTimeout(() => {
      setShowNotification(false);
    }, 5000);
  };

  useEffect(() => {
    if (checkSessionExpiration()) {
      setError('Tu sesión anterior ha expirado. Por favor, inicia sesión nuevamente.');
    }
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-green-900 via-green-800 to-red-900"></div>
      
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-0 left-0 w-72 h-72 bg-white rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse"></div>
        <div className="absolute top-0 right-0 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-red-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse animation-delay-4000"></div>
      </div>

      {showNotification && (
        <div className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-green-600 to-green-700 text-white px-6 py-4 shadow-xl animate-slideDown backdrop-blur-sm">
          <div className="flex items-center justify-between max-w-4xl mx-auto">
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
              <span className="font-medium">Estamos contactando con el administrador del sistema...</span>
            </div>
            <button
              onClick={() => setShowNotification(false)}
              className="text-white hover:text-gray-200 ml-4 p-1 rounded-full hover:bg-white/20 transition-colors"
            >
              <FontAwesomeIcon icon={faTimes} />
            </button>
          </div>
        </div>
      )}

      <div className="relative z-10 flex flex-col lg:flex-row w-full max-w-6xl mx-4">
        
        <div className="w-full lg:w-1/2 flex items-center justify-center p-6 lg:p-12">
          <div className="w-full max-w-md bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/20">
            
            <div className="mb-8 text-center">
              <div className="mb-6">
                <h1 className="text-5xl font-black bg-gradient-to-r from-green-700 via-green-600 to-red-600 bg-clip-text text-transparent mb-2">
                  SAID
                </h1>
                <div className="w-20 h-1 bg-gradient-to-r from-green-600 to-red-600 mx-auto rounded-full"></div>
              </div>
              <p className="text-2xl font-bold text-gray-800 mb-2">Bienvenido</p>
              <p className="text-gray-600 text-sm">Sistema de Administración de Incidencias Delictivas</p>
            </div>

            {error && (
              <div className="bg-red-50 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded-lg relative mb-6 text-sm shadow-sm">
                <div className="flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  <span className="font-medium">{error}</span>
                </div>
              </div>
            )}

            <form className="space-y-6" onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div className="group">
                  <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
                    Usuario
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none group-focus-within:text-green-600 transition-colors">
                      <FontAwesomeIcon icon={faUser} className="text-gray-400 text-lg" />
                    </div>
                    <input
                      id="username"
                      name="username"
                      type="text"
                      required
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      autoComplete="username"
                      className="block w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 text-base text-gray-900 transition-all duration-300 hover:border-gray-400"
                      placeholder="Ingrese su usuario"
                    />
                  </div>
                </div>

                <div className="group">
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                    Contraseña
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none group-focus-within:text-green-600 transition-colors">
                      <FontAwesomeIcon icon={faLock} className="text-gray-400 text-lg" />
                    </div>
                    <input
                      id="password"
                      name="password"
                      type={showPassword ? 'text' : 'password'}
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      autoComplete="current-password"
                      className="block w-full pl-12 pr-12 py-3 border border-gray-300 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 text-base text-gray-900 transition-all duration-300 hover:border-gray-400"
                      placeholder="Ingrese su contraseña"
                    />
                    <div
                      className="absolute inset-y-0 right-0 pr-4 flex items-center cursor-pointer text-gray-400 hover:text-green-600 transition-colors"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      <FontAwesomeIcon icon={showPassword ? faEyeSlash : faEye} className="text-lg" />
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center">
                  <input
                    id="remember-me"
                    name="remember-me"
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    autoComplete="off"
                    className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                  />
                  <label htmlFor="remember-me" className="ml-2 block text-gray-700 font-medium">
                    Recordar sesión
                  </label>
                </div>
                <div className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                  {rememberMe ? 'Permanente' : `${SESSION_TIMEOUT_SECONDS}s`}
                </div>
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full relative overflow-hidden bg-gradient-to-r from-green-700 via-green-600 to-red-600 text-white py-3 px-4 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none transition-all duration-300"
                >
                  <span className="relative z-10">
                    {loading ? (
                      <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        Verificando...
                      </div>
                    ) : (
                      'Iniciar Sesión'
                    )}
                  </span>
                  <div className="absolute inset-0 bg-gradient-to-r from-green-800 via-green-700 to-red-700 opacity-0 hover:opacity-100 transition-opacity duration-300"></div>
                </button>
              </div>
            </form>

            <div className="mt-8 text-center">
              <p className="text-sm text-gray-600 mb-3">¿Necesitas ayuda para acceder?</p>
              <button 
                onClick={handleHelpClick}
                className="inline-flex items-center font-medium text-green-700 hover:text-green-800 transition duration-300 underline decoration-2 underline-offset-2 hover:decoration-green-600"
              >
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Solicitar asistencia
              </button>
            </div>
          </div>
        </div>

        <div className="hidden lg:flex lg:w-1/2 items-center justify-center p-8">
          <div className="relative">
            <div className="absolute inset-0 bg-white/20 backdrop-blur-sm rounded-3xl transform rotate-3"></div>
            <div className="relative bg-white/90 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/30">
              <img
                src={policiaLoginImage}
                alt="Policía Nacional del Perú"
                className="w-full h-full object-contain filter drop-shadow-lg"
              />
              <div className="absolute -bottom-2 -right-2 w-full h-full bg-gradient-to-br from-green-600/20 to-red-600/20 rounded-3xl -z-10"></div>
            </div>
          </div>
        </div>
      </div>

      <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-green-600 via-yellow-500 to-red-600"></div>
    </div>
  );
};

export default Login;
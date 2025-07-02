// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import LoginPage from './auth/Login';
import RequireAuth from './Components/RequireAuth';
import RedirectIfAuth from './Components/RedirectIfAuth';
import UserDashboard from './users/UserDashboard';
import SideBar from './Components/layout/SideBar';
import UsersPage from './pages/users/UsersPage';
import CreateUser from './pages/users/CreateUser';
import EditUser from './pages/users/EditUser';
import ViewUser from './pages/users/ViewUser';
import GroupsPage from './pages/groups/GroupsPage';
import CreateGroup from './pages/groups/CreateGroup';
import EditGroup from './pages/groups/EditGroup';
import ViewGroup from './pages/groups/ViewGroup';
import { useSessionManager } from './hooks/useSessionManager';
import { AuthProvider, useAuthContext } from './contexts/AuthContext';
import PermissionGuard from './Components/PermissionGuard';
import AuthLoadingWrapper from './Components/AuthLoadingWrapper';
import ProductionPage from './pages/production/ProductionPage';
import IncidentPage from './pages/incident/IncidentPage';

// Componente de loading mientras se verifica la autenticación
const AuthLoadingScreen = () => (
  <div className="min-h-screen bg-gradient-to-br from-green-600 to-emerald-600 flex items-center justify-center">
    <div className="flex flex-col items-center space-y-6">
      <div className="animate-spin rounded-full h-20 w-20 border-4 border-white border-t-transparent shadow-lg"></div>
      <div className="text-center">
        <h2 className="text-2xl font-bold text-white mb-2">Verificando acceso...</h2>
        <p className="text-green-100">Por favor espera un momento</p>
      </div>
    </div>
  </div>
);

// Componente que maneja las rutas protegidas
const ProtectedRoutes = () => {
  return (
    <div className="flex min-h-screen">
      <SideBar />
      <div className="flex-1 bg-gray-50 p-6">
        <Routes>
          {/* Dashboard */}
          <Route path="dashboard" element={<UserDashboard />} />
          
          {/* Rutas de Usuarios - Con protección de permisos */}
          <Route path="users" element={
            <PermissionGuard>
              <UsersPage />
            </PermissionGuard>
          } />
          <Route path="users/create" element={
            <PermissionGuard>
              <CreateUser />
            </PermissionGuard>
          } />
          <Route path="users/edit/:id" element={
            <PermissionGuard>
              <EditUser />
            </PermissionGuard>
          } />
          <Route path="users/view/:id" element={
            <PermissionGuard>
              <ViewUser />
            </PermissionGuard>
          } />
          
          {/* Rutas de Grupos - Con protección de permisos */}
          <Route path="groups" element={
            <PermissionGuard>
              <GroupsPage />
            </PermissionGuard>
          } />
          <Route path="groups/create" element={
            <PermissionGuard>
              <CreateGroup />
            </PermissionGuard>
          } />
          <Route path="groups/edit/:id" element={
            <PermissionGuard>
              <EditGroup />
            </PermissionGuard>
          } />
          <Route path="groups/view/:id" element={
            <PermissionGuard>
              <ViewGroup />
            </PermissionGuard>
          } />
          
          {/* OFAD - Producción e Incidencias */}
          <Route path="ofad/produccion/*" element={
            <PermissionGuard>
              <ProductionPage />
            </PermissionGuard>
          } />
          <Route path="ofad/incidencias" element={
            <PermissionGuard>
              <IncidentPage />
            </PermissionGuard>
          } />

          {/* DIVREINT - Con protección de permisos */}
          <Route
            path="divreint"
            element={
              <PermissionGuard>
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">DIVREINT</h2>
                  <p className="text-gray-600">División de Inteligencia en construcción...</p>
                </div>
              </PermissionGuard>
            }
          />
          
          {/* Admin */}
          <Route
            path="admin"
            element={
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Administración</h2>
                <p className="text-gray-600">Panel de administración en construcción...</p>
              </div>
            }
          />
          
          {/* Ruta por defecto para rutas no encontradas */}
          <Route path="*" element={<Navigate to="dashboard" replace />} />
        </Routes>
      </div>
    </div>
  );
};

function AppContent() {
  useSessionManager();
  const { user, loading } = useAuthContext();

  // Mostrar loading mientras se verifica la autenticación
  if (loading) {
    return <AuthLoadingScreen />;
  }

  return (
    <Routes>
      {/* Ruta de login */}
      <Route
        path="/login"
        element={
          <RedirectIfAuth>
            <LoginPage />
          </RedirectIfAuth>
        }
      />

      {/* Ruta raíz - redirige según el estado de autenticación */}
      <Route 
        path="/" 
        element={
          user ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />
        } 
      />

      {/* Todas las rutas protegidas */}
      <Route
        path="/*"
        element={
          <RequireAuth>
            <ProtectedRoutes />
          </RequireAuth>
        }
      />
    </Routes>
  );
}

function AppWrapper() {
  return (
    <AuthProvider>
      <Router>
        <AuthLoadingWrapper>
          <AppContent />
        </AuthLoadingWrapper>
      </Router>
    </AuthProvider>
  );
}

export default AppWrapper;
import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { 
  DocumentTextIcon, 
  UserGroupIcon,
  BeakerIcon,
  ScaleIcon,
  HomeIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

// Importar páginas - Solo las que existen
import RQPage from './personas/RQPage';
import RQForm from './personas/forms/RQForm';

const ProductionPage = () => {
  const location = useLocation();

  // Función para verificar si una ruta está activa
  const isActiveRoute = (path) => {
    return location.pathname.includes(path);
  };

  // Componente de navegación lateral
  const Navigation = () => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center space-x-3 mb-6">
        <div className="bg-green-100 p-2 rounded-lg">
          <DocumentTextIcon className="h-6 w-6 text-green-600" />
        </div>
        <div>
          <h2 className="text-lg font-bold text-gray-900">Módulo de Producción</h2>
          <p className="text-sm text-gray-600">Formularios Policiales</p>
        </div>
      </div>

      <nav className="space-y-2">
        {/* Dashboard */}
        <Link
          to="/ofad/produccion"
          className={`flex items-center space-x-3 px-3 py-2 rounded-md transition-colors ${
            location.pathname === '/ofad/produccion'
              ? 'bg-green-100 text-green-700'
              : 'text-gray-600 hover:bg-gray-50'
          }`}
        >
          <HomeIcon className="h-5 w-5" />
          <span>Dashboard</span>
        </Link>

        {/* Sección Personas */}
        <div className="pt-4">
          <div className="flex items-center space-x-2 px-3 py-2">
            <UserGroupIcon className="h-4 w-4 text-gray-400" />
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
              Formularios de Personas
            </span>
          </div>
          
          <Link
            to="/ofad/produccion/personas/rq"
            className={`flex items-center space-x-3 px-3 py-2 rounded-md transition-colors ml-4 ${
              isActiveRoute('/personas/rq')
                ? 'bg-red-100 text-red-700'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <DocumentTextIcon className="h-4 w-4" />
            <span>RQ - Requisitorias</span>
          </Link>
          
          <div className="flex items-center space-x-3 px-3 py-2 text-gray-400 ml-4">
            <DocumentTextIcon className="h-4 w-4" />
            <span>Detenidos (En construcción)</span>
          </div>
          
          <div className="flex items-center space-x-3 px-3 py-2 text-gray-400 ml-4">
            <DocumentTextIcon className="h-4 w-4" />
            <span>Menores (En construcción)</span>
          </div>
        </div>

        {/* Sección Drogas - Envoltorios */}
        <div className="pt-4">
          <div className="flex items-center space-x-2 px-3 py-2">
            <BeakerIcon className="h-4 w-4 text-gray-400" />
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
              Envoltorios de Drogas
            </span>
          </div>
          
          <div className="flex items-center space-x-3 px-3 py-2 text-gray-400 ml-4">
            <BeakerIcon className="h-4 w-4" />
            <span>ENV PBC (En construcción)</span>
          </div>
          
          <div className="flex items-center space-x-3 px-3 py-2 text-gray-400 ml-4">
            <BeakerIcon className="h-4 w-4" />
            <span>ENV CC (En construcción)</span>
          </div>
          
          <div className="flex items-center space-x-3 px-3 py-2 text-gray-400 ml-4">
            <BeakerIcon className="h-4 w-4" />
            <span>ENV Marihuana (En construcción)</span>
          </div>
        </div>

        {/* Sección Drogas - Kilogramos */}
        <div className="pt-4">
          <div className="flex items-center space-x-2 px-3 py-2">
            <ScaleIcon className="h-4 w-4 text-gray-400" />
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
              Kilogramos de Drogas
            </span>
          </div>
          
          <div className="flex items-center space-x-3 px-3 py-2 text-gray-400 ml-4">
            <ScaleIcon className="h-4 w-4" />
            <span>KG PBC (En construcción)</span>
          </div>
          
          <div className="flex items-center space-x-3 px-3 py-2 text-gray-400 ml-4">
            <ScaleIcon className="h-4 w-4" />
            <span>KG CC (En construcción)</span>
          </div>
          
          <div className="flex items-center space-x-3 px-3 py-2 text-gray-400 ml-4">
            <ScaleIcon className="h-4 w-4" />
            <span>KG Marihuana (En construcción)</span>
          </div>
        </div>

        {/* Sección Reportes */}
        <div className="pt-4">
          <div className="flex items-center space-x-2 px-3 py-2">
            <ChartBarIcon className="h-4 w-4 text-gray-400" />
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
              Reportes y Estadísticas
            </span>
          </div>
          
          <div className="flex items-center space-x-3 px-3 py-2 text-gray-400 ml-4">
            <ChartBarIcon className="h-4 w-4" />
            <span>Reportes (En construcción)</span>
          </div>
        </div>
      </nav>
    </div>
  );

  // Dashboard principal
  const Dashboard = () => (
    <div className="space-y-6">
      {/* Encabezado del Dashboard */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Dashboard de Producción</h1>
            <p className="text-gray-600">Resumen general de formularios policiales</p>
          </div>
          <div className="bg-green-100 p-3 rounded-lg">
            <DocumentTextIcon className="h-8 w-8 text-green-600" />
          </div>
        </div>
      </div>

      {/* Tarjetas de resumen */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* RQ */}
        <Link
          to="/ofad/produccion/personas/rq"
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
        >
          <div className="flex items-center">
            <div className="bg-red-100 p-3 rounded-lg">
              <DocumentTextIcon className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Requisitorias</p>
              <p className="text-2xl font-bold text-gray-900">--</p>
            </div>
          </div>
        </Link>

        {/* Detenidos */}
        <div className="bg-gray-50 rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="bg-gray-200 p-3 rounded-lg">
              <UserGroupIcon className="h-6 w-6 text-gray-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-400">Detenidos</p>
              <p className="text-sm text-gray-400">En construcción</p>
            </div>
          </div>
        </div>

        {/* Envoltorios */}
        <div className="bg-gray-50 rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="bg-gray-200 p-3 rounded-lg">
              <BeakerIcon className="h-6 w-6 text-gray-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-400">Envoltorios</p>
              <p className="text-sm text-gray-400">En construcción</p>
            </div>
          </div>
        </div>

        {/* Kilogramos */}
        <div className="bg-gray-50 rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="bg-gray-200 p-3 rounded-lg">
              <ScaleIcon className="h-6 w-6 text-gray-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-400">Kilogramos</p>
              <p className="text-sm text-gray-400">En construcción</p>
            </div>
          </div>
        </div>
      </div>

      {/* Información adicional */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Estado del Módulo</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">✅ Completado</h4>
            <ul className="space-y-1 text-sm text-gray-600">
              <li>• Backend completo (APIs, modelos, validaciones)</li>
              <li>• RQ - Formulario de Requisitorias</li>
              <li>• Navegación y estructura base</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-2">🚧 En construcción</h4>
            <ul className="space-y-1 text-sm text-gray-600">
              <li>• Formulario de Detenidos</li>
              <li>• Formulario de Menores</li>
              <li>• 8 Formularios de Drogas</li>
              <li>• Reportes y estadísticas</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex space-x-6">
      {/* Navegación lateral */}
      <div className="w-80 flex-shrink-0">
        <Navigation />
      </div>

      {/* Contenido principal */}
      <div className="flex-1">
        <Routes>
          {/* Dashboard principal */}
          <Route path="/" element={<Dashboard />} />
          
          {/* Rutas de RQ */}
          <Route path="/personas/rq" element={<RQPage />} />
          <Route path="/personas/rq/create" element={<RQForm />} />
          <Route path="/personas/rq/edit/:id" element={<RQForm />} />
          
          {/* Rutas en construcción */}
          <Route path="*" element={
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Módulo en Construcción</h2>
              <p className="text-gray-600">Esta funcionalidad estará disponible próximamente.</p>
              <Link
                to="/ofad/produccion"
                className="mt-4 inline-flex items-center text-green-600 hover:text-green-800"
              >
                ← Volver al Dashboard
              </Link>
            </div>
          } />
        </Routes>
      </div>
    </div>
  );
};

export default ProductionPage;
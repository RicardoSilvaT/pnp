import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Home,
  Users,
  Shield,
  Settings,
  FileText,
  Building2,
  ChevronLeft,
  ChevronRight,
  LogOut,
  ShieldAlert,
  FileBarChart,
} from "lucide-react";
import { useAuthContext } from '../../contexts/AuthContext';
import { getMenuItemsForUser } from '../../utils/permissions';
import {
  formatFullName,
  getUserInitials,
} from '../../utils/userConstants';

const SideBar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [manualOfadToggle, setManualOfadToggle] = useState(false);
  const [manualAdminToggle, setManualAdminToggle] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  
  // Obtener contexto con valores por defecto
  const getAuthContext = () => {
    try {
      return useAuthContext();
    } catch (error) {
      console.log('AuthContext no disponible, usando valores por defecto');
      return {
        user: null,
        loading: false,
        logout: () => {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          navigate('/login');
        }
      };
    }
  };

  const { user, loading, logout } = getAuthContext();

  // Determinar expansión automática de menús
  const getAutoExpansion = () => {
    const adminPaths = ["/admin", "/users", "/groups", "/app/admin", "/app/users", "/app/groups"];
    const ofadPaths = ["/ofad", "/app/ofad"];
    
    return {
      admin: adminPaths.some(path => location.pathname.startsWith(path)),
      ofad: ofadPaths.some(path => location.pathname.startsWith(path))
    };
  };

  const autoExpansion = getAutoExpansion();
  const adminExpanded = autoExpansion.admin || manualAdminToggle;
  const ofadExpanded = autoExpansion.ofad || manualOfadToggle;

  // Efecto para manejar el margen del body
  useEffect(() => {
    const body = document.body;
    body.classList.remove('ml-64', 'ml-20');
    body.classList.add(isCollapsed ? 'ml-20' : 'ml-64', 'transition-all', 'duration-200');
    
    return () => {
      body.classList.remove('ml-64', 'ml-20', 'transition-all', 'duration-200');
    };
  }, [isCollapsed]);

  // Funciones helper
  const toggleSidebar = () => setIsCollapsed(!isCollapsed);
  const getInitials = () => user ? getUserInitials(user) : 'U';
  const getFullName = () => user ? formatFullName(user) : 'Usuario';
  const handleNavigation = (href) => navigate(href);
  const handleLogout = () => {
    navigate('/login');
    logout();
  };

  // Verificar si una ruta está activa
  const isActive = (href) => {
    if (href === "/") {
      const dashboardPaths = ["/", "/dashboard", "/app/dashboard"];
      return dashboardPaths.includes(location.pathname);
    }
    const normalizedPath = location.pathname.replace('/app/', '/');
    return normalizedPath.startsWith(href) || location.pathname.startsWith(href);
  };

  // Mapeo de iconos
  const iconMap = { Home, FileText, Building2, Users, Shield, Settings };

  // Obtener datos del menú
  const { mainMenu, adminMenu, ofadMenu, showAdminSection } = getMenuItemsForUser(user);

  // Componente de tooltip
  const Tooltip = ({ children, text, show }) => (
    <div className="relative group">
      {children}
      {show && (
        <div className="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 whitespace-nowrap z-50 shadow-lg min-w-max">
          <div className="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-1 w-0 h-0 border-t-4 border-b-4 border-r-4 border-transparent border-r-gray-900"></div>
          {typeof text === 'string' ? text : <div>{text}</div>}
        </div>
      )}
    </div>
  );

  // Componente de item de menú
  const MenuItem = ({ item, className = "" }) => {
    // Asignar iconos específicos basados en el texto del label
    let IconComponent;
    
    if (item.label.toLowerCase().includes('incidencia')) {
      IconComponent = ShieldAlert; // Icono de escudo con alerta para incidencias delictivas
    } else if (item.label.toLowerCase().includes('producción') || item.label.toLowerCase().includes('produccion')) {
      IconComponent = FileBarChart; // Icono de archivo con gráfico para datos policiales
    } else {
      IconComponent = iconMap[item.icon] || FileText; // Icono por defecto
    }
    
    const active = isActive(item.href);
    
    return (
      <li>
        <Tooltip text={item.label} show={isCollapsed}>
          <button
            onClick={() => handleNavigation(item.href)}
            className={`
              relative w-full flex items-center px-3 py-3 rounded-lg transition-all duration-200 group
              ${active 
                ? "bg-green-50 text-green-600 border-l-4 border-green-600" 
                : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
              }
              ${className}
            `}
          >
            <IconComponent
              className={`flex-shrink-0 ${isCollapsed ? "mx-auto" : "mr-3"}`}
              size={className.includes('text-sm') ? 16 : 20}
            />
            {!isCollapsed && <span className="font-medium">{item.label}</span>}
          </button>
        </Tooltip>
      </li>
    );
  };

  // Componente de sección expandible - versión simplificada
  const ExpandableSection = ({ 
    title, 
    icon: Icon, 
    expanded, 
    onToggle, 
    items, 
    children 
  }) => (
    <li>
      <Tooltip text={title} show={isCollapsed}>
        <button
          onClick={onToggle}
          className={`
            relative w-full flex items-center justify-between px-3 py-3 rounded-lg transition-all duration-200 group
            ${expanded
              ? "bg-green-50 text-green-600 border-l-4 border-green-600"
              : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
            }
          `}
        >
          <div className="flex items-center">
            <Icon className={`flex-shrink-0 ${isCollapsed ? "mx-auto" : "mr-3"}`} size={20} />
            {!isCollapsed && <span className="font-medium">{title}</span>}
          </div>
          {!isCollapsed && (
            <ChevronRight
              className={`transform transition-transform duration-200 ${expanded ? "rotate-90" : ""}`}
              size={16}
            />
          )}
        </button>
      </Tooltip>

      {expanded && !isCollapsed && items?.length > 0 && (
        <ul className="mt-2 ml-6 space-y-1 animate-in fade-in-0 slide-in-from-top-1 duration-200">
          {children}
        </ul>
      )}
    </li>
  );

  // Loading state
  if (loading && !user) {
    return (
      <div className={`bg-white shadow-xl border-r border-gray-200 h-screen flex flex-col transition-all duration-200 ease-out flex-shrink-0 fixed left-0 top-0 z-40 ${isCollapsed ? "w-20" : "w-64"}`}>
        <div className="h-12 bg-gradient-to-r from-green-700 to-green-600"></div>
        <div className="h-20 border-b border-gray-200 bg-gradient-to-r from-green-600 to-green-700 flex items-center justify-center">
          <div className="animate-pulse">
            <div className="w-12 h-12 bg-green-500 rounded-full"></div>
          </div>
        </div>
        <div className="flex-1 p-4">
          <div className="space-y-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-10 bg-gray-200 rounded animate-pulse"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white shadow-xl border-r border-gray-200 h-screen flex flex-col transition-all duration-200 ease-out flex-shrink-0 fixed left-0 top-0 z-40 ${isCollapsed ? "w-20 overflow-hidden" : "w-64"}`}>
      
      {/* Toggle Button */}
      <div className="h-12 bg-gradient-to-r from-green-700 to-green-600 flex items-center justify-end pr-4 border-b border-green-800 flex-shrink-0">
        <button
          onClick={toggleSidebar}
          className="w-8 h-8 text-white rounded-full flex items-center justify-center hover:bg-white hover:bg-opacity-20 transition-all duration-200 group"
        >
          {isCollapsed ? (
            <ChevronRight size={16} className="group-hover:scale-110 transition-transform" />
          ) : (
            <ChevronLeft size={16} className="group-hover:scale-110 transition-transform" />
          )}
        </button>
      </div>

      {/* User Header */}
      <div className="border-b border-gray-200 bg-gradient-to-r from-green-600 to-green-700 p-4 flex-shrink-0">
        {!isCollapsed ? (
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center flex-shrink-0">
              <span className="text-green-600 font-bold text-lg">{getInitials()}</span>
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-white font-medium text-sm truncate">{getFullName()}</div>
              {user?.email && <div className="text-green-100 text-xs truncate">{user.email}</div>}
              {user?.groups?.length > 0 && (
                <div className="text-green-200 text-xs truncate font-medium">
                  {user.groups.join(', ')}
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="flex justify-center">
            <Tooltip 
              text={
                <div>
                  <div className="font-medium">{getFullName()}</div>
                  {user?.email && <div className="text-xs text-gray-300 mt-1">{user.email}</div>}
                  {user?.groups?.length > 0 && (
                    <div className="text-xs text-gray-400 font-medium mt-1">
                      {user.groups.join(', ')}
                    </div>
                  )}
                </div>
              } 
              show={true}
            >
              <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
                <span className="text-green-600 font-bold text-sm">{getInitials()}</span>
              </div>
            </Tooltip>
          </div>
        )}
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 py-6 overflow-y-auto overflow-x-hidden">
        <ul className="space-y-2 px-3">
          {/* Main Menu */}
          {mainMenu.map((item, index) => (
            <MenuItem key={index} item={item} />
          ))}

          {/* OFAD Menu */}
          {ofadMenu.length > 0 && (
            <ExpandableSection
              title="OFAD"
              icon={FileText}
              expanded={ofadExpanded}
              onToggle={() => setManualOfadToggle(!manualOfadToggle)}
              items={ofadMenu}
            >
              {ofadMenu.map((item, index) => (
                <MenuItem key={index} item={item} className="text-sm" />
              ))}
            </ExpandableSection>
          )}

          {/* Admin Menu */}
          {showAdminSection && (
            <ExpandableSection
              title="Administración"
              icon={Settings}
              expanded={adminExpanded}
              onToggle={() => setManualAdminToggle(!manualAdminToggle)}
              items={adminMenu}
            >
              {adminMenu.map((item, index) => (
                <MenuItem key={index} item={item} className="text-sm" />
              ))}
            </ExpandableSection>
          )}
        </ul>
      </nav>

      {/* Logout Section */}
      <div className="border-t border-gray-200 p-3 flex-shrink-0">
        <Tooltip text="Cerrar Sesión" show={isCollapsed}>
          <button
            onClick={handleLogout}
            className="relative w-full flex items-center px-3 py-3 rounded-lg text-gray-600 hover:bg-red-50 hover:text-red-600 transition-all duration-200"
          >
            <LogOut className={`flex-shrink-0 ${isCollapsed ? "mx-auto" : "mr-3"}`} size={20} />
            {!isCollapsed && <span className="font-medium">Cerrar Sesión</span>}
          </button>
        </Tooltip>
      </div>
    </div>
  );
};

export default SideBar;
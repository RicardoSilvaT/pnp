// src/utils/permissions.js

// Definir qué grupos tienen acceso a qué rutas
export const ROUTE_PERMISSIONS = {
  // Dashboard - Todos tienen acceso
  '/dashboard': {
    groups: ['Administrador', 'Analista', 'Visualizador'],
  },

  // OFAD - Producción e Incidencias - Administrador y Analista
  '/ofad/produccion': {
    groups: ['Administrador', 'Analista'],
  },
  '/ofad/incidencias': {
    groups: ['Administrador', 'Analista'],
  },

  // DIVREINT - Administrador y Analista
  '/divreint': {
    groups: ['Administrador', 'Analista'],
  },

  // Usuarios - Solo Administrador
  '/users': {
    groups: ['Administrador'],
  },

  // Grupos - Solo Administrador
  '/groups': {
    groups: ['Administrador'],
  },
};

// Verificar si un usuario tiene acceso a una ruta basado en su grupo
export const canAccessRoute = (path, user) => {
  // Superusuarios tienen acceso a todo
  if (user?.is_superuser) return true;

  // Buscar la configuración de permisos para la ruta
  const routeConfig = Object.entries(ROUTE_PERMISSIONS).find(([route]) =>
    path.startsWith(route)
  );

  if (!routeConfig) {
    // Si no hay configuración, permitir acceso
    return true;
  }

  const [, config] = routeConfig;

  // Verificar si el usuario tiene alguno de los grupos requeridos
  const hasRequiredGroup = config.groups.length === 0 ||
    config.groups.some(group => user?.groups?.includes(group));

  return hasRequiredGroup;
};

// Obtener rutas permitidas para el menú basado en grupos
export const getMenuItemsForUser = (user) => {
  const menuItems = [
    {
      icon: 'Home',
      label: 'Dashboard',
      href: '/dashboard',
      alwaysShow: true,
    },
    // OFAD será gestionado como submenú, no incluir aquí
    {
      icon: 'Building2',
      label: 'DIVREINT',
      href: '/divreint',
      groups: ['Administrador', 'Analista'],
    },
  ];

  const ofadMenuItems = [
    {
      icon: 'FileText',
      label: 'Producción',
      href: '/ofad/produccion',
      groups: ['Administrador', 'Analista'],
    },
    {
      icon: 'FileText',
      label: 'Incidencias',
      href: '/ofad/incidencias',
      groups: ['Administrador', 'Analista'],
    },
  ];

  const adminMenuItems = [
    {
      icon: 'Users',
      label: 'Usuarios',
      href: '/users',
      groups: ['Administrador'],
    },
    {
      icon: 'Shield',
      label: 'Grupos',
      href: '/groups',
      groups: ['Administrador'],
    },
  ];

  // Filtrar items del menú basado solo en grupos
  const filterMenuItems = (items) => {
    return items.filter(item => {
      // Si es superusuario, mostrar todo
      if (user?.is_superuser) return true;

      // Si siempre se debe mostrar
      if (item.alwaysShow) return true;

      // Verificar grupos
      const hasGroup = !item.groups ||
        item.groups.some(group => user?.groups?.includes(group));

      return hasGroup;
    });
  };

  const mainMenu = filterMenuItems(menuItems);
  const adminMenu = filterMenuItems(adminMenuItems);
  const ofadMenu = filterMenuItems(ofadMenuItems);

  return {
    mainMenu,
    adminMenu,
    ofadMenu,
    showAdminSection: adminMenu.length > 0 && (
      user?.is_superuser || user?.groups?.includes('Administrador')
    ),
  };
};

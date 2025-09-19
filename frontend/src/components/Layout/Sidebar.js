import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { usePlugins } from '../../contexts/PluginContext';
import { 
  LayoutDashboard, 
  FileText, 
  File, 
  Puzzle, 
  Users, 
  Settings,
  ChevronRight
} from 'lucide-react';

const Sidebar = () => {
  const location = useLocation();
  const { user, hasRole } = useAuth();
  const { executeHook } = usePlugins();
  const [menuItems, setMenuItems] = useState([]);

  const defaultMenuItems = [
    {
      title: 'Dashboard',
      path: '/admin',
      icon: LayoutDashboard,
      roles: ['admin', 'editor', 'author']
    },
    {
      title: 'Posts',
      path: '/admin/posts',
      icon: FileText,
      roles: ['admin', 'editor', 'author']
    },
    {
      title: 'Pages',
      path: '/admin/pages',
      icon: File,
      roles: ['admin', 'editor']
    },
    {
      title: 'Plugins',
      path: '/admin/plugins',
      icon: Puzzle,
      roles: ['admin']
    },
    {
      title: 'Users',
      path: '/admin/users',
      icon: Users,
      roles: ['admin']
    },
    {
      title: 'Settings',
      path: '/admin/settings',
      icon: Settings,
      roles: ['admin', 'editor', 'author']
    }
  ];

  useEffect(() => {
    // Initialize with default menu items
    setMenuItems(defaultMenuItems);
    
    // Allow plugins to modify menu items (but don't send React components)
    const loadPluginMenuItems = async () => {
      try {
        // Only send serializable data to the backend
        const menuData = defaultMenuItems.map(item => ({
          title: item.title,
          path: item.path,
          roles: item.roles
        }));
        
        const result = await executeHook('admin_menu', menuData);
        
        // If result is valid, merge with default items
        if (Array.isArray(result)) {
          // Map back to include icons
          const enhancedItems = result.map(item => {
            const defaultItem = defaultMenuItems.find(d => d.path === item.path);
            return {
              ...item,
              icon: defaultItem?.icon || Settings
            };
          });
          setMenuItems(enhancedItems);
        }
      } catch (error) {
        console.error('Error loading plugin menu items:', error);
        // Fallback to default menu items
        setMenuItems(defaultMenuItems);
      }
    };
    
    loadPluginMenuItems();
  }, [executeHook]);

  const isActive = (path) => {
    return location.pathname === path;
  };

  const canAccessMenuItem = (item) => {
    return item.roles.includes(user?.role);
  };

  return (
    <div className="w-64 bg-white border-r border-gray-200 h-screen flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-gray-200">
        <h1 className="text-xl font-bold text-gray-900">CMS Pro</h1>
        <p className="text-sm text-gray-500">Plugin-Powered CMS</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {menuItems
          .filter(canAccessMenuItem)
          .map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                  isActive(item.path)
                    ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-600'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <Icon className="w-5 h-5 mr-3" />
                {item.title}
                {isActive(item.path) && (
                  <ChevronRight className="w-4 h-4 ml-auto" />
                )}
              </Link>
            );
          })}
      </nav>

      {/* User Info */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center space-x-3">
          <img
            src={user?.avatar}
            alt={user?.name}
            className="w-8 h-8 rounded-full"
          />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">
              {user?.name}
            </p>
            <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
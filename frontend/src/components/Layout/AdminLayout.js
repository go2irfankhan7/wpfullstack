import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { usePlugins } from '../../contexts/PluginContext';
import Sidebar from './Sidebar';
import Header from './Header';

const AdminLayout = ({ children }) => {
  const { user } = useAuth();
  const { executeHook } = usePlugins();

  // Allow plugins to modify the admin layout
  const layoutData = executeHook('admin_layout', { user, children });

  return (
    <div className="min-h-screen bg-gray-50 flex">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 p-6">
          {layoutData.children || children}
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;
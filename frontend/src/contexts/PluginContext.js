import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PluginContext = createContext();

export const usePlugins = () => {
  const context = useContext(PluginContext);
  if (!context) {
    throw new Error('usePlugins must be used within a PluginProvider');
  }
  return context;
};

export const PluginProvider = ({ children }) => {
  const [plugins, setPlugins] = useState([]);
  const [activePlugins, setActivePlugins] = useState([]);
  const [pluginHooks, setPluginHooks] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadPlugins();
    loadActivePlugins();
    loadPluginHooks();
  }, []);

  const loadPlugins = async () => {
    try {
      const response = await axios.get(`${API}/plugins`);
      setPlugins(response.data);
    } catch (error) {
      console.error('Error loading plugins:', error);
    }
  };

  const loadActivePlugins = async () => {
    try {
      const response = await axios.get(`${API}/plugins/active`);
      setActivePlugins(response.data.map(p => p.id));
    } catch (error) {
      console.error('Error loading active plugins:', error);
    }
  };

  const loadPluginHooks = async () => {
    try {
      const response = await axios.get(`${API}/plugins/hooks`);
      setPluginHooks(response.data);
    } catch (error) {
      console.error('Error loading plugin hooks:', error);
    }
  };

  const activatePlugin = async (pluginId) => {
    try {
      setIsLoading(true);
      await axios.put(`${API}/plugins/${pluginId}/activate`);
      
      // Update local state
      setActivePlugins(prev => [...prev, pluginId]);
      
      // Update plugin status in plugins list
      setPlugins(prev => prev.map(p => 
        p.id === pluginId ? { ...p, status: 'active' } : p
      ));
      
      // Reload hooks
      await loadPluginHooks();
      
      return true;
    } catch (error) {
      console.error('Error activating plugin:', error);
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const deactivatePlugin = async (pluginId) => {
    try {
      setIsLoading(true);
      await axios.put(`${API}/plugins/${pluginId}/deactivate`);
      
      // Update local state
      setActivePlugins(prev => prev.filter(id => id !== pluginId));
      
      // Update plugin status in plugins list
      setPlugins(prev => prev.map(p => 
        p.id === pluginId ? { ...p, status: 'installed' } : p
      ));
      
      // Reload hooks
      await loadPluginHooks();
      
      return true;
    } catch (error) {
      console.error('Error deactivating plugin:', error);
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const executeHook = async (hookName, data = {}) => {
    try {
      const response = await axios.post(`${API}/plugins/execute-hook`, {
        hook_name: hookName,
        data: data
      });
      
      return response.data.data || data;
    } catch (error) {
      console.error('Error executing hook:', error);
      return data;
    }
  };

  const isPluginActive = (pluginId) => {
    return activePlugins.includes(pluginId);
  };

  const installPlugin = async (pluginFile) => {
    try {
      setIsLoading(true);
      const formData = new FormData();
      formData.append('plugin_file', pluginFile);
      
      const response = await axios.post(`${API}/plugins/install`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      console.log('Plugin installation response:', response.data);
      
      // Reload plugins
      await loadPlugins();
      
      return true;
    } catch (error) {
      console.error('Error installing plugin:', error);
      
      // Check if it's a specific error response
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      } else if (error.response?.status === 403) {
        throw new Error('Admin access required to install plugins');
      } else if (error.response?.status === 400) {
        throw new Error('Invalid plugin file format or structure');
      } else {
        throw new Error('Failed to install plugin. Please check your connection and try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const value = {
    plugins,
    activePlugins,
    activatePlugin,
    deactivatePlugin,
    isPluginActive,
    installPlugin,
    executeHook,
    isLoading,
    loadPlugins
  };

  return (
    <PluginContext.Provider value={value}>
      {children}
    </PluginContext.Provider>
  );
};
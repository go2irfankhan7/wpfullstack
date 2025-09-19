import React, { createContext, useContext, useState, useEffect } from 'react';
import { mockPlugins } from '../data/mock';

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

  useEffect(() => {
    // Load plugins and active state from storage
    setPlugins(mockPlugins);
    const storedActivePlugins = localStorage.getItem('cms_active_plugins');
    if (storedActivePlugins) {
      setActivePlugins(JSON.parse(storedActivePlugins));
    }
  }, []);

  const activatePlugin = (pluginId) => {
    if (!activePlugins.includes(pluginId)) {
      const newActivePlugins = [...activePlugins, pluginId];
      setActivePlugins(newActivePlugins);
      localStorage.setItem('cms_active_plugins', JSON.stringify(newActivePlugins));
      
      // Execute plugin activation hook
      const plugin = plugins.find(p => p.id === pluginId);
      if (plugin && plugin.hooks) {
        registerPluginHooks(pluginId, plugin.hooks);
      }
    }
  };

  const deactivatePlugin = (pluginId) => {
    const newActivePlugins = activePlugins.filter(id => id !== pluginId);
    setActivePlugins(newActivePlugins);
    localStorage.setItem('cms_active_plugins', JSON.stringify(newActivePlugins));
    
    // Remove plugin hooks
    setPluginHooks(prev => {
      const newHooks = { ...prev };
      Object.keys(newHooks).forEach(hookName => {
        newHooks[hookName] = newHooks[hookName].filter(hook => hook.pluginId !== pluginId);
      });
      return newHooks;
    });
  };

  const registerPluginHooks = (pluginId, hooks) => {
    setPluginHooks(prev => {
      const newHooks = { ...prev };
      Object.entries(hooks).forEach(([hookName, hookFunction]) => {
        if (!newHooks[hookName]) {
          newHooks[hookName] = [];
        }
        newHooks[hookName].push({
          pluginId,
          execute: hookFunction
        });
      });
      return newHooks;
    });
  };

  const executeHook = (hookName, data = {}) => {
    const hooks = pluginHooks[hookName] || [];
    let result = data;
    
    hooks.forEach(hook => {
      try {
        const hookResult = hook.execute(result);
        if (hookResult !== undefined) {
          result = hookResult;
        }
      } catch (error) {
        console.error(`Error executing hook ${hookName} from plugin ${hook.pluginId}:`, error);
      }
    });
    
    return result;
  };

  const isPluginActive = (pluginId) => {
    return activePlugins.includes(pluginId);
  };

  const installPlugin = (plugin) => {
    setPlugins(prev => [...prev, plugin]);
  };

  const value = {
    plugins,
    activePlugins,
    activatePlugin,
    deactivatePlugin,
    isPluginActive,
    installPlugin,
    executeHook,
    registerPluginHooks
  };

  return (
    <PluginContext.Provider value={value}>
      {children}
    </PluginContext.Provider>
  );
};
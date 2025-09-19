import os
import json
import importlib
import zipfile
import tempfile
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from models import Plugin, PluginHookExecution, PluginHookResult, PluginStatus
from database import find_documents, find_document, update_document, insert_document
import logging

logger = logging.getLogger(__name__)

class PluginManager:
    """Revolutionary plugin management system for CMS Pro"""
    
    def __init__(self):
        self.loaded_plugins: Dict[str, Any] = {}
        self.hook_registry: Dict[str, List[Callable]] = {}
        self.plugin_hooks: Dict[str, Dict[str, Any]] = {}
        self.plugins_dir = Path("/app/plugins")
        self.plugins_dir.mkdir(exist_ok=True)

    async def initialize(self):
        """Initialize plugin system and load active plugins"""
        try:
            await self.load_active_plugins()
            logger.info("Plugin system initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing plugin system: {e}")

    async def install_plugin(self, plugin_file: bytes, plugin_metadata: Dict[str, Any]) -> str:
        """Install a plugin from uploaded ZIP file"""
        try:
            # Create temporary directory for extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                zip_path = temp_path / "plugin.zip"
                
                # Save uploaded file
                with open(zip_path, "wb") as f:
                    f.write(plugin_file)
                
                # Extract and validate plugin
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_path)
                
                # Validate plugin structure
                plugin_json_path = temp_path / "plugin.json"
                if not plugin_json_path.exists():
                    raise ValueError("Plugin must contain plugin.json file")
                
                # Load plugin metadata
                with open(plugin_json_path, 'r') as f:
                    plugin_config = json.load(f)
                
                # Validate required fields
                required_fields = ['name', 'version', 'description', 'author']
                for field in required_fields:
                    if field not in plugin_config:
                        raise ValueError(f"Plugin missing required field: {field}")
                
                # Create plugin directory
                plugin_id = plugin_config['name'].lower().replace(' ', '-')
                plugin_dir = self.plugins_dir / plugin_id
                
                if plugin_dir.exists():
                    # Update existing plugin
                    import shutil
                    shutil.rmtree(plugin_dir)
                
                plugin_dir.mkdir(exist_ok=True)
                
                # Copy plugin files
                import shutil
                for item in temp_path.iterdir():
                    if item.name != "plugin.zip":
                        if item.is_dir():
                            shutil.copytree(item, plugin_dir / item.name)
                        else:
                            shutil.copy2(item, plugin_dir)
                
                # Save plugin to database
                plugin_data = {
                    "_id": plugin_id,
                    "name": plugin_config['name'],
                    "description": plugin_config['description'],
                    "version": plugin_config['version'],
                    "author": plugin_config['author'],
                    "category": plugin_config.get('category', 'General'),
                    "status": PluginStatus.INSTALLED,
                    "price": plugin_config.get('price', 'Free'),
                    "features": plugin_config.get('features', []),
                    "dependencies": plugin_config.get('dependencies', []),
                    "hooks": plugin_config.get('hooks', {}),
                    "settings_schema": plugin_config.get('settings_schema', {}),
                    "settings": {},
                    "install_path": str(plugin_dir),
                    "icon": plugin_config.get('icon'),
                    "screenshots": plugin_config.get('screenshots', [])
                }
                
                # Check if plugin already exists
                existing_plugin = await find_document("plugins", {"_id": plugin_id})
                if existing_plugin:
                    await update_document("plugins", {"_id": plugin_id}, plugin_data)
                else:
                    await insert_document("plugins", plugin_data)
                
                logger.info(f"Plugin {plugin_config['name']} installed successfully")
                return plugin_id
                
        except Exception as e:
            logger.error(f"Error installing plugin: {e}")
            raise ValueError(f"Plugin installation failed: {str(e)}")

    async def activate_plugin(self, plugin_id: str) -> bool:
        """Activate a plugin and load its hooks"""
        try:
            plugin_doc = await find_document("plugins", {"_id": plugin_id})
            if not plugin_doc:
                raise ValueError("Plugin not found")
            
            if plugin_doc["status"] == PluginStatus.ACTIVE:
                return True
            
            plugin = Plugin(**plugin_doc)
            
            # Check dependencies
            await self._check_plugin_dependencies(plugin.dependencies)
            
            # Load plugin hooks
            await self._load_plugin_hooks(plugin)
            
            # Update plugin status
            await update_document(
                "plugins", 
                {"_id": plugin_id}, 
                {"status": PluginStatus.ACTIVE}
            )
            
            self.loaded_plugins[plugin_id] = plugin
            
            logger.info(f"Plugin {plugin.name} activated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error activating plugin {plugin_id}: {e}")
            return False

    async def deactivate_plugin(self, plugin_id: str) -> bool:
        """Deactivate a plugin and unload its hooks"""
        try:
            plugin_doc = await find_document("plugins", {"_id": plugin_id})
            if not plugin_doc:
                return False
            
            # Remove plugin hooks
            self._unload_plugin_hooks(plugin_id)
            
            # Update plugin status
            await update_document(
                "plugins",
                {"_id": plugin_id},
                {"status": PluginStatus.INSTALLED}
            )
            
            if plugin_id in self.loaded_plugins:
                del self.loaded_plugins[plugin_id]
            
            logger.info(f"Plugin {plugin_id} deactivated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error deactivating plugin {plugin_id}: {e}")
            return False

    async def uninstall_plugin(self, plugin_id: str) -> bool:
        """Uninstall a plugin completely"""
        try:
            # First deactivate
            await self.deactivate_plugin(plugin_id)
            
            # Remove plugin files
            plugin_doc = await find_document("plugins", {"_id": plugin_id})
            if plugin_doc and plugin_doc.get("install_path"):
                plugin_dir = Path(plugin_doc["install_path"])
                if plugin_dir.exists():
                    import shutil
                    shutil.rmtree(plugin_dir)
            
            # Remove from database
            from database import delete_document
            await delete_document("plugins", {"_id": plugin_id})
            
            logger.info(f"Plugin {plugin_id} uninstalled successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error uninstalling plugin {plugin_id}: {e}")
            return False

    async def execute_hook(self, hook_name: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute all registered hooks for a given hook name"""
        result = data.copy() if data else {}
        executed_hooks = []
        
        try:
            if hook_name in self.hook_registry:
                for hook_func in self.hook_registry[hook_name]:
                    try:
                        hook_result = await hook_func(result) if callable(hook_func) else result
                        if hook_result is not None:
                            result = hook_result
                        executed_hooks.append({
                            "plugin_id": getattr(hook_func, 'plugin_id', 'unknown'),
                            "success": True
                        })
                    except Exception as e:
                        logger.error(f"Error executing hook {hook_name}: {e}")
                        executed_hooks.append({
                            "plugin_id": getattr(hook_func, 'plugin_id', 'unknown'),
                            "success": False,
                            "error": str(e)
                        })
            
            return {
                "data": result,
                "executed_hooks": executed_hooks
            }
            
        except Exception as e:
            logger.error(f"Error in hook execution system: {e}")
            return {"data": result, "executed_hooks": []}

    async def get_plugin_settings(self, plugin_id: str) -> Dict[str, Any]:
        """Get plugin settings"""
        plugin_doc = await find_document("plugins", {"_id": plugin_id})
        if not plugin_doc:
            return {}
        return plugin_doc.get("settings", {})

    async def update_plugin_settings(self, plugin_id: str, settings: Dict[str, Any]) -> bool:
        """Update plugin settings"""
        try:
            result = await update_document(
                "plugins",
                {"_id": plugin_id},
                {"settings": settings}
            )
            return result
        except Exception as e:
            logger.error(f"Error updating plugin settings: {e}")
            return False

    async def load_active_plugins(self):
        """Load all active plugins on system startup"""
        try:
            active_plugins = await find_documents(
                "plugins", 
                {"status": PluginStatus.ACTIVE}
            )
            
            for plugin_doc in active_plugins:
                plugin = Plugin(**plugin_doc)
                await self._load_plugin_hooks(plugin)
                self.loaded_plugins[plugin.id] = plugin
            
            logger.info(f"Loaded {len(active_plugins)} active plugins")
            
        except Exception as e:
            logger.error(f"Error loading active plugins: {e}")

    async def _load_plugin_hooks(self, plugin: Plugin):
        """Load hooks from a plugin"""
        try:
            if not plugin.hooks:
                return
            
            plugin_dir = Path(plugin.install_path) if plugin.install_path else None
            if not plugin_dir or not plugin_dir.exists():
                logger.warning(f"Plugin directory not found for {plugin.name}")
                return
            
            # Load backend hooks if they exist
            backend_hooks_file = plugin_dir / "backend" / "hooks.py"
            if backend_hooks_file.exists():
                await self._load_backend_hooks(plugin, backend_hooks_file)
            
            # Store plugin hooks for frontend
            self.plugin_hooks[plugin.id] = plugin.hooks
            
        except Exception as e:
            logger.error(f"Error loading hooks for plugin {plugin.name}: {e}")

    async def _load_backend_hooks(self, plugin: Plugin, hooks_file: Path):
        """Load backend hooks from Python file"""
        try:
            # Dynamically import the hooks module
            spec = importlib.util.spec_from_file_location(
                f"{plugin.id}_hooks", 
                hooks_file
            )
            hooks_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(hooks_module)
            
            # Register hook functions
            for hook_name, hook_config in plugin.hooks.items():
                if hasattr(hooks_module, hook_name):
                    hook_func = getattr(hooks_module, hook_name)
                    hook_func.plugin_id = plugin.id
                    
                    if hook_name not in self.hook_registry:
                        self.hook_registry[hook_name] = []
                    
                    self.hook_registry[hook_name].append(hook_func)
            
        except Exception as e:
            logger.error(f"Error loading backend hooks for {plugin.name}: {e}")

    def _unload_plugin_hooks(self, plugin_id: str):
        """Unload hooks for a plugin"""
        try:
            # Remove from hook registry
            for hook_name in list(self.hook_registry.keys()):
                self.hook_registry[hook_name] = [
                    hook for hook in self.hook_registry[hook_name]
                    if getattr(hook, 'plugin_id', None) != plugin_id
                ]
                
                # Clean up empty hook lists
                if not self.hook_registry[hook_name]:
                    del self.hook_registry[hook_name]
            
            # Remove from plugin hooks
            if plugin_id in self.plugin_hooks:
                del self.plugin_hooks[plugin_id]
                
        except Exception as e:
            logger.error(f"Error unloading hooks for plugin {plugin_id}: {e}")

    async def _check_plugin_dependencies(self, dependencies: List[str]):
        """Check if plugin dependencies are met"""
        for dep in dependencies:
            dep_plugin = await find_document(
                "plugins", 
                {"name": dep, "status": PluginStatus.ACTIVE}
            )
            if not dep_plugin:
                raise ValueError(f"Dependency not met: {dep}")

    def get_frontend_hooks(self) -> Dict[str, Dict[str, Any]]:
        """Get all frontend hooks for client-side execution"""
        return self.plugin_hooks

# Global plugin manager instance
plugin_manager = PluginManager()
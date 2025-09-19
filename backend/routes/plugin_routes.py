from fastapi import APIRouter, HTTPException, status, Depends, Query, UploadFile, File
from typing import List, Optional, Dict, Any

from models import (
    PluginResponse, PluginCreate, PluginUpdate, PluginStatus,
    PluginHookExecution, User, UserRole
)
from auth import get_current_active_user, require_role
from plugin_system import plugin_manager
from database import find_documents, find_document, update_document
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/plugins", tags=["plugins"])

@router.get("", response_model=List[PluginResponse])
async def get_plugins(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    status: Optional[PluginStatus] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Get all plugins"""
    try:
        filter_dict = {}
        
        if category:
            filter_dict["category"] = category
            
        if status:
            filter_dict["status"] = status
            
        if search:
            filter_dict["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
                {"author": {"$regex": search, "$options": "i"}}
            ]
        
        plugins = await find_documents(
            "plugins",
            filter_dict,
            sort=[("created_at", -1)],
            skip=skip,
            limit=limit
        )
        
        return [PluginResponse(**plugin) for plugin in plugins]
        
    except Exception as e:
        logger.error(f"Error fetching plugins: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch plugins"
        )

@router.get("/active", response_model=List[PluginResponse])
async def get_active_plugins(current_user: User = Depends(get_current_active_user)):
    """Get all active plugins"""
    try:
        active_plugins = await find_documents(
            "plugins",
            {"status": PluginStatus.ACTIVE},
            sort=[("name", 1)]
        )
        
        return [PluginResponse(**plugin) for plugin in active_plugins]
        
    except Exception as e:
        logger.error(f"Error fetching active plugins: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch active plugins"
        )

@router.get("/hooks")
async def get_plugin_hooks(current_user: User = Depends(get_current_active_user)):
    """Get all frontend hooks from active plugins"""
    try:
        return plugin_manager.get_frontend_hooks()
    except Exception as e:
        logger.error(f"Error fetching plugin hooks: {e}")
        return {}

@router.get("/{plugin_id}", response_model=PluginResponse)
async def get_plugin(
    plugin_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get plugin by ID"""
    try:
        plugin = await find_document("plugins", {"_id": plugin_id})
        if not plugin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found"
            )
        
        return PluginResponse(**plugin)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching plugin {plugin_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch plugin"
        )

@router.post("/install")
async def install_plugin(
    plugin_file: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Install a plugin from ZIP file (admin only)"""
    try:
        if not plugin_file.filename.endswith('.zip'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Plugin file must be a ZIP archive"
            )
        
        # Read file contents
        file_contents = await plugin_file.read()
        
        # Install plugin
        plugin_id = await plugin_manager.install_plugin(file_contents, {})
        
        logger.info(f"Plugin {plugin_id} installed by {current_user.email}")
        
        return {"message": f"Plugin {plugin_id} installed successfully", "plugin_id": plugin_id}
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error installing plugin: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to install plugin"
        )

@router.put("/{plugin_id}/activate")
async def activate_plugin(
    plugin_id: str,
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Activate a plugin (admin only)"""
    try:
        success = await plugin_manager.activate_plugin(plugin_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to activate plugin"
            )
        
        logger.info(f"Plugin {plugin_id} activated by {current_user.email}")
        
        return {"message": f"Plugin {plugin_id} activated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error activating plugin {plugin_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to activate plugin"
        )

@router.put("/{plugin_id}/deactivate")
async def deactivate_plugin(
    plugin_id: str,
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Deactivate a plugin (admin only)"""
    try:
        success = await plugin_manager.deactivate_plugin(plugin_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Plugin not found or already deactivated"
            )
        
        logger.info(f"Plugin {plugin_id} deactivated by {current_user.email}")
        
        return {"message": f"Plugin {plugin_id} deactivated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deactivating plugin {plugin_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate plugin"
        )

@router.delete("/{plugin_id}")
async def uninstall_plugin(
    plugin_id: str,
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Uninstall a plugin (admin only)"""
    try:
        success = await plugin_manager.uninstall_plugin(plugin_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to uninstall plugin"
            )
        
        logger.info(f"Plugin {plugin_id} uninstalled by {current_user.email}")
        
        return {"message": f"Plugin {plugin_id} uninstalled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uninstalling plugin {plugin_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to uninstall plugin"
        )

@router.get("/{plugin_id}/settings")
async def get_plugin_settings(
    plugin_id: str,
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Get plugin settings (admin only)"""
    try:
        settings = await plugin_manager.get_plugin_settings(plugin_id)
        return {"settings": settings}
        
    except Exception as e:
        logger.error(f"Error fetching plugin settings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch plugin settings"
        )

@router.put("/{plugin_id}/settings")
async def update_plugin_settings(
    plugin_id: str,
    settings_data: Dict[str, Any],
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Update plugin settings (admin only)"""
    try:
        success = await plugin_manager.update_plugin_settings(
            plugin_id, 
            settings_data.get("settings", {})
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found"
            )
        
        logger.info(f"Plugin {plugin_id} settings updated by {current_user.email}")
        
        return {"message": "Plugin settings updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating plugin settings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update plugin settings"
        )

@router.post("/execute-hook")
async def execute_plugin_hook(
    hook_execution: PluginHookExecution,
    current_user: User = Depends(get_current_active_user)
):
    """Execute a plugin hook"""
    try:
        result = await plugin_manager.execute_hook(
            hook_execution.hook_name,
            hook_execution.data
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error executing plugin hook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to execute plugin hook"
        )
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional

from models import UserResponse, UserCreate, UserUpdate, UserRole, User
from auth import get_current_active_user, require_role, get_password_hash, has_permission
from database import (
    find_documents, find_document, insert_document, 
    update_document, delete_document, count_documents
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    role: Optional[UserRole] = None,
    search: Optional[str] = None,
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    """Get all users (requires editor role or higher)"""
    try:
        filter_dict = {"is_active": True}
        
        if role:
            filter_dict["role"] = role
            
        if search:
            filter_dict["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}}
            ]
        
        users = await find_documents(
            "users",
            filter_dict,
            sort=[("created_at", -1)],
            skip=skip,
            limit=limit
        )
        
        return [UserResponse(**user) for user in users]
        
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch users"
        )

@router.get("/stats")
async def get_user_stats(current_user: User = Depends(require_role(UserRole.ADMIN))):
    """Get user statistics (admin only)"""
    try:
        total_users = await count_documents("users", {"is_active": True})
        admin_count = await count_documents("users", {"role": UserRole.ADMIN, "is_active": True})
        editor_count = await count_documents("users", {"role": UserRole.EDITOR, "is_active": True})
        author_count = await count_documents("users", {"role": UserRole.AUTHOR, "is_active": True})
        
        return {
            "total": total_users,
            "admin": admin_count,
            "editor": editor_count,
            "author": author_count
        }
        
    except Exception as e:
        logger.error(f"Error fetching user stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user statistics"
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get user by ID"""
    try:
        # Users can view their own profile, editors+ can view any profile
        if user_id != current_user.id and not has_permission(current_user, UserRole.EDITOR):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this user"
            )
        
        user = await find_document("users", {"_id": user_id, "is_active": True})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(**user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user"
        )

@router.post("", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Create a new user (admin only)"""
    try:
        # Check if user already exists
        existing_user = await find_document("users", {"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        user_dict = user_data.dict()
        user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))
        user_dict["is_active"] = True
        user_dict["avatar"] = f"https://api.dicebear.com/7.x/avataaars/svg?seed={user_data.email}"
        
        user_id = await insert_document("users", user_dict)
        user_dict["id"] = user_id
        
        logger.info(f"User created: {user_data.email} by {current_user.email}")
        
        return UserResponse(**user_dict)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update user"""
    try:
        # Users can update their own profile, admins can update any profile
        if user_id != current_user.id and not has_permission(current_user, UserRole.ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this user"
            )
        
        # Check if user exists
        existing_user = await find_document("users", {"_id": user_id, "is_active": True})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Prepare update data
        update_dict = {k: v for k, v in user_data.dict().items() if v is not None}
        
        # Only admins can change roles
        if "role" in update_dict and not has_permission(current_user, UserRole.ADMIN):
            del update_dict["role"]
        
        if update_dict:
            await update_document("users", {"_id": user_id}, update_dict)
            
            # Get updated user
            updated_user = await find_document("users", {"_id": user_id})
            logger.info(f"User {user_id} updated by {current_user.email}")
            
            return UserResponse(**updated_user)
        
        return UserResponse(**existing_user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Delete user (admin only)"""
    try:
        # Prevent self-deletion
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account"
            )
        
        # Check if user exists
        user = await find_document("users", {"_id": user_id, "is_active": True})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Soft delete (deactivate)
        await update_document("users", {"_id": user_id}, {"is_active": False})
        
        logger.info(f"User {user_id} deleted by {current_user.email}")
        
        return {"message": "User deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )

@router.put("/{user_id}/role")
async def update_user_role(
    user_id: str,
    role_data: dict,
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Update user role (admin only)"""
    try:
        new_role = role_data.get("role")
        if not new_role or new_role not in [r.value for r in UserRole]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role specified"
            )
        
        # Check if user exists
        user = await find_document("users", {"_id": user_id, "is_active": True})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        await update_document("users", {"_id": user_id}, {"role": new_role})
        
        logger.info(f"User {user_id} role updated to {new_role} by {current_user.email}")
        
        return {"message": f"User role updated to {new_role}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user role"
        )
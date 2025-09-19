from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any, List

from models import DashboardStats, User, UserRole, ContentStatus, PluginStatus
from auth import get_current_active_user
from database import count_documents, find_documents, find_document
from plugin_system import plugin_manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_user: User = Depends(get_current_active_user)):
    """Get dashboard statistics"""
    try:
        # Base stats
        filter_dict = {}
        if current_user.role == UserRole.AUTHOR:
            # Authors can only see their own content stats
            filter_dict["author_id"] = current_user.id

        total_posts = await count_documents("posts", filter_dict)
        total_pages = await count_documents("pages", {} if current_user.role != UserRole.AUTHOR else {"author_id": current_user.id})
        total_users = await count_documents("users", {"is_active": True}) if current_user.role in [UserRole.ADMIN, UserRole.EDITOR] else 0
        active_plugins = await count_documents("plugins", {"status": PluginStatus.ACTIVE})

        # Recent activity
        recent_activity = []
        
        # Recent posts
        recent_posts = await find_documents(
            "posts",
            filter_dict,
            sort=[("created_at", -1)],
            limit=3
        )
        
        for post in recent_posts:
            author = await find_document("users", {"_id": post["author_id"]}) if "author_id" in post else None
            recent_activity.append({
                "type": "post",
                "message": f"Post '{post['title']}' was {post['status']}",
                "time": post["created_at"].isoformat() if "created_at" in post else "",
                "icon": "FileText",
                "author": author["name"] if author else "Unknown"
            })

        # Recent plugin activations (admin/editor only)
        if current_user.role in [UserRole.ADMIN, UserRole.EDITOR]:
            recent_plugins = await find_documents(
                "plugins",
                {"status": PluginStatus.ACTIVE},
                sort=[("updated_at", -1)],
                limit=2
            )
            
            for plugin in recent_plugins:
                recent_activity.append({
                    "type": "plugin",
                    "message": f"Plugin '{plugin['name']}' was activated",
                    "time": plugin.get("updated_at", plugin.get("created_at", "")).isoformat() if plugin.get("updated_at") else "",
                    "icon": "Puzzle"
                })

        # Allow plugins to modify dashboard stats
        hook_result = await plugin_manager.execute_hook("dashboard_stats", {
            "total_posts": total_posts,
            "total_pages": total_pages,
            "total_users": total_users,
            "active_plugins": active_plugins,
            "recent_activity": recent_activity,
            "current_user": {
                "id": current_user.id,
                "role": current_user.role.value,
                "name": current_user.name
            }
        })

        stats_data = hook_result.get("data", {
            "total_posts": total_posts,
            "total_pages": total_pages,
            "total_users": total_users,
            "active_plugins": active_plugins,
            "recent_activity": recent_activity
        })

        return DashboardStats(**stats_data)

    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch dashboard statistics"
        )

@router.get("/activity")
async def get_recent_activity(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user)
):
    """Get recent activity feed"""
    try:
        activity_feed = []

        # Recent posts
        post_filter = {}
        if current_user.role == UserRole.AUTHOR:
            post_filter["author_id"] = current_user.id

        recent_posts = await find_documents(
            "posts",
            post_filter,
            sort=[("created_at", -1)],
            limit=limit // 2
        )

        for post in recent_posts:
            author = await find_document("users", {"_id": post["author_id"]}) if "author_id" in post else None
            activity_feed.append({
                "id": post["id"],
                "type": "post_created",
                "title": f"New post: {post['title']}",
                "description": f"Created by {author['name'] if author else 'Unknown'}",
                "timestamp": post["created_at"],
                "icon": "FileText",
                "url": f"/admin/posts/{post['id']}"
            })

        # Recent pages (editor+ only)
        if current_user.role in [UserRole.ADMIN, UserRole.EDITOR]:
            recent_pages = await find_documents(
                "pages",
                {},
                sort=[("created_at", -1)],
                limit=limit // 4
            )

            for page in recent_pages:
                author = await find_document("users", {"_id": page["author_id"]}) if "author_id" in page else None
                activity_feed.append({
                    "id": page["id"],
                    "type": "page_created",
                    "title": f"New page: {page['title']}",
                    "description": f"Created by {author['name'] if author else 'Unknown'}",
                    "timestamp": page["created_at"],
                    "icon": "File",
                    "url": f"/admin/pages/{page['id']}"
                })

        # Recent users (admin only)
        if current_user.role == UserRole.ADMIN:
            recent_users = await find_documents(
                "users",
                {"is_active": True},
                sort=[("created_at", -1)],
                limit=limit // 4
            )

            for user in recent_users:
                activity_feed.append({
                    "id": user["id"],
                    "type": "user_registered",
                    "title": f"New user: {user['name']}",
                    "description": f"Role: {user['role']}",
                    "timestamp": user["created_at"],
                    "icon": "Users",
                    "url": f"/admin/users/{user['id']}"
                })

        # Sort by timestamp and limit
        activity_feed.sort(key=lambda x: x["timestamp"], reverse=True)
        activity_feed = activity_feed[:limit]

        # Allow plugins to modify activity feed
        hook_result = await plugin_manager.execute_hook("activity_feed", {
            "activity_feed": activity_feed,
            "current_user": {
                "id": current_user.id,
                "role": current_user.role.value,
                "name": current_user.name
            }
        })

        return hook_result.get("data", {"activity_feed": activity_feed})

    except Exception as e:
        logger.error(f"Error fetching activity feed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch activity feed"
        )

@router.get("/quick-stats")
async def get_quick_stats(current_user: User = Depends(get_current_active_user)):
    """Get quick statistics for dashboard widgets"""
    try:
        stats = {}

        # Content stats
        if current_user.role == UserRole.AUTHOR:
            stats["my_posts"] = await count_documents("posts", {"author_id": current_user.id})
            stats["my_published_posts"] = await count_documents("posts", {
                "author_id": current_user.id,
                "status": ContentStatus.PUBLISHED
            })
        else:
            stats["total_posts"] = await count_documents("posts", {})
            stats["published_posts"] = await count_documents("posts", {"status": ContentStatus.PUBLISHED})
            stats["draft_posts"] = await count_documents("posts", {"status": ContentStatus.DRAFT})

        # Admin/Editor specific stats
        if current_user.role in [UserRole.ADMIN, UserRole.EDITOR]:
            stats["total_pages"] = await count_documents("pages", {})
            stats["published_pages"] = await count_documents("pages", {"status": ContentStatus.PUBLISHED})

        # Admin specific stats
        if current_user.role == UserRole.ADMIN:
            stats["total_users"] = await count_documents("users", {"is_active": True})
            stats["total_plugins"] = await count_documents("plugins", {})
            stats["active_plugins"] = await count_documents("plugins", {"status": PluginStatus.ACTIVE})

        # Allow plugins to add custom stats
        hook_result = await plugin_manager.execute_hook("quick_stats", {
            "stats": stats,
            "current_user": {
                "id": current_user.id,
                "role": current_user.role.value,
                "name": current_user.name
            }
        })

        return hook_result.get("data", {"stats": stats})

    except Exception as e:
        logger.error(f"Error fetching quick stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch quick statistics"
        )
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
import re

from models import (
    PostResponse, PostCreate, PostUpdate, ContentStatus, User, UserRole,
    PageResponse, PageCreate, PageUpdate
)
from auth import get_current_active_user, require_role, can_edit_content
from database import (
    find_documents, find_document, insert_document,
    update_document, delete_document, count_documents
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["content"])

# Posts Routes
posts_router = APIRouter(prefix="/posts")

@posts_router.get("", response_model=List[PostResponse])
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[ContentStatus] = None,
    category: Optional[str] = None,
    author_id: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Get all posts with filtering"""
    try:
        filter_dict = {}
        
        # Authors can only see their own posts unless they have higher permissions
        if current_user.role == UserRole.AUTHOR:
            filter_dict["author_id"] = current_user.id
        elif author_id:
            filter_dict["author_id"] = author_id
            
        if status:
            filter_dict["status"] = status
            
        if category:
            filter_dict["category"] = category
            
        if search:
            filter_dict["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}},
                {"tags": {"$in": [search]}}
            ]
        
        posts = await find_documents(
            "posts",
            filter_dict,
            sort=[("created_at", -1)],
            skip=skip,
            limit=limit
        )
        
        # Add author names
        for post in posts:
            if post.get("author_id"):
                author = await find_document("users", {"_id": post["author_id"]})
                post["author"] = author["name"] if author else "Unknown Author"
        
        return [PostResponse(**post) for post in posts]
        
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch posts"
        )

@posts_router.get("/stats")
async def get_post_stats(current_user: User = Depends(get_current_active_user)):
    """Get post statistics"""
    try:
        filter_dict = {}
        if current_user.role == UserRole.AUTHOR:
            filter_dict["author_id"] = current_user.id
            
        total_posts = await count_documents("posts", filter_dict)
        published_posts = await count_documents("posts", {**filter_dict, "status": ContentStatus.PUBLISHED})
        draft_posts = await count_documents("posts", {**filter_dict, "status": ContentStatus.DRAFT})
        private_posts = await count_documents("posts", {**filter_dict, "status": ContentStatus.PRIVATE})
        
        return {
            "total": total_posts,
            "published": published_posts,
            "draft": draft_posts,
            "private": private_posts
        }
        
    except Exception as e:
        logger.error(f"Error fetching post stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch post statistics"
        )

@posts_router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get post by ID"""
    try:
        post = await find_document("posts", {"_id": post_id})
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Check if user can view this post
        if (post["status"] == ContentStatus.PRIVATE and 
            not await can_edit_content(current_user, post["author_id"])):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this post"
            )
        
        # Add author name
        author = await find_document("users", {"_id": post["author_id"]})
        post["author"] = author["name"] if author else "Unknown Author"
        
        return PostResponse(**post)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching post {post_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch post"
        )

@posts_router.post("", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new post"""
    try:
        post_dict = post_data.dict()
        post_dict["author_id"] = current_user.id
        
        # Generate excerpt if not provided
        if not post_dict.get("excerpt") and post_dict.get("content"):
            # Remove HTML tags and truncate
            clean_content = re.sub('<[^<]+?>', '', post_dict["content"])
            post_dict["excerpt"] = clean_content[:150] + "..." if len(clean_content) > 150 else clean_content
        
        post_id = await insert_document("posts", post_dict)
        post_dict["id"] = post_id
        post_dict["author"] = current_user.name
        
        logger.info(f"Post created: {post_data.title} by {current_user.email}")
        
        return PostResponse(**post_dict)
        
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create post"
        )

@posts_router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update post"""
    try:
        # Check if post exists
        existing_post = await find_document("posts", {"_id": post_id})
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Check permissions
        if not await can_edit_content(current_user, existing_post["author_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to edit this post"
            )
        
        # Prepare update data
        update_dict = {k: v for k, v in post_data.dict().items() if v is not None}
        
        # Update excerpt if content changed
        if "content" in update_dict and "excerpt" not in update_dict:
            clean_content = re.sub('<[^<]+?>', '', update_dict["content"])
            update_dict["excerpt"] = clean_content[:150] + "..." if len(clean_content) > 150 else clean_content
        
        if update_dict:
            await update_document("posts", {"_id": post_id}, update_dict)
            
            # Get updated post
            updated_post = await find_document("posts", {"_id": post_id})
            author = await find_document("users", {"_id": updated_post["author_id"]})
            updated_post["author"] = author["name"] if author else "Unknown Author"
            
            logger.info(f"Post {post_id} updated by {current_user.email}")
            
            return PostResponse(**updated_post)
        
        return PostResponse(**existing_post)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating post {post_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update post"
        )

@posts_router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete post"""
    try:
        # Check if post exists
        post = await find_document("posts", {"_id": post_id})
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Check permissions
        if not await can_edit_content(current_user, post["author_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this post"
            )
        
        await delete_document("posts", {"_id": post_id})
        
        logger.info(f"Post {post_id} deleted by {current_user.email}")
        
        return {"message": "Post deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting post {post_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete post"
        )

# Pages Routes
pages_router = APIRouter(prefix="/pages")

@pages_router.get("", response_model=List[PageResponse])
async def get_pages(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[ContentStatus] = None,
    search: Optional[str] = None,
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    """Get all pages (requires editor role)"""
    try:
        filter_dict = {}
        
        if status:
            filter_dict["status"] = status
            
        if search:
            filter_dict["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}},
                {"slug": {"$regex": search, "$options": "i"}}
            ]
        
        pages = await find_documents(
            "pages",
            filter_dict,
            sort=[("created_at", -1)],
            skip=skip,
            limit=limit
        )
        
        # Add author names
        for page in pages:
            if page.get("author_id"):
                author = await find_document("users", {"_id": page["author_id"]})
                page["author"] = author["name"] if author else "Unknown Author"
        
        return [PageResponse(**page) for page in pages]
        
    except Exception as e:
        logger.error(f"Error fetching pages: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch pages"
        )

def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

@pages_router.post("", response_model=PageResponse)
async def create_page(
    page_data: PageCreate,
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    """Create a new page (requires editor role)"""
    try:
        page_dict = page_data.dict()
        page_dict["author_id"] = current_user.id
        
        # Generate slug if not provided
        if not page_dict.get("slug"):
            page_dict["slug"] = generate_slug(page_dict["title"])
        
        # Ensure slug is unique
        existing_page = await find_document("pages", {"slug": page_dict["slug"]})
        if existing_page:
            # Append timestamp to make it unique
            from datetime import datetime
            timestamp = int(datetime.utcnow().timestamp())
            page_dict["slug"] = f"{page_dict['slug']}-{timestamp}"
        
        page_id = await insert_document("pages", page_dict)
        page_dict["id"] = page_id
        page_dict["author"] = current_user.name
        
        logger.info(f"Page created: {page_data.title} by {current_user.email}")
        
        return PageResponse(**page_dict)
        
    except Exception as e:
        logger.error(f"Error creating page: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create page"
        )

# Include routers
router.include_router(posts_router)
router.include_router(pages_router)
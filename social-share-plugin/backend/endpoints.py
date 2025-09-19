# Custom API endpoints for Social Media Share & Like Plugin
from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict, Any, List
from datetime import datetime
import logging
from .hooks import track_like_event, track_share_event, get_platform_breakdown, get_engagement_trends

logger = logging.getLogger(__name__)

# Create router for social share endpoints
social_router = APIRouter(prefix="/social", tags=["social-share"])

@social_router.post("/posts/{post_id}/like")
async def like_post(
    post_id: str,
    like_data: Dict[str, Any] = Body(...),
    # current_user: User = Depends(get_current_active_user)  # Uncomment when integrated
):
    """Like or unlike a post"""
    try:
        action = like_data.get('action', 'like')  # 'like' or 'unlike'
        user_id = "current_user.id"  # Would get from authenticated user
        
        if action not in ['like', 'unlike']:
            raise HTTPException(status_code=400, detail="Action must be 'like' or 'unlike'")
        
        # Track the like/unlike event
        event_result = await track_like_event(post_id, user_id, action)
        
        # Here you would update the post's like count in the database
        # For now, we'll simulate it
        new_like_count = like_data.get('current_count', 0)
        if action == 'like':
            new_like_count += 1
        else:
            new_like_count = max(0, new_like_count - 1)
        
        return {
            "success": True,
            "action": action,
            "new_like_count": new_like_count,
            "event_id": event_result.get('event_id'),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing like for post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process like")

@social_router.post("/posts/{post_id}/share")
async def share_post(
    post_id: str,
    share_data: Dict[str, Any] = Body(...),
    # current_user: User = Depends(get_current_active_user)  # Optional - can track anonymous shares
):
    """Track social media share"""
    try:
        platform = share_data.get('platform')
        if not platform:
            raise HTTPException(status_code=400, detail="Platform is required")
        
        valid_platforms = ['facebook', 'twitter', 'linkedin', 'whatsapp', 'telegram', 'reddit', 'pinterest']
        if platform not in valid_platforms:
            raise HTTPException(status_code=400, detail=f"Invalid platform. Must be one of: {valid_platforms}")
        
        user_id = "current_user.id if current_user else None"  # Anonymous shares allowed
        
        # Track the share event
        event_result = await track_share_event(post_id, platform, user_id)
        
        # Here you would update the post's share count in the database
        # Increment both total shares and platform-specific shares
        new_share_count = share_data.get('current_count', 0) + 1
        
        return {
            "success": True,
            "platform": platform,
            "new_share_count": new_share_count,
            "event_id": event_result.get('event_id'),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error tracking share for post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to track share")

@social_router.get("/posts/{post_id}/stats")
async def get_post_social_stats(
    post_id: str,
    # current_user: User = Depends(get_current_active_user)
):
    """Get social media statistics for a specific post"""
    try:
        # In a real implementation, this would query the database
        # For now, we'll return mock data
        import random
        
        stats = {
            "post_id": post_id,
            "likes": random.randint(10, 500),
            "total_shares": random.randint(5, 200),
            "platform_shares": {
                "facebook": random.randint(0, 50),
                "twitter": random.randint(0, 40), 
                "linkedin": random.randint(0, 25),
                "whatsapp": random.randint(0, 60),
                "telegram": random.randint(0, 15),
                "reddit": random.randint(0, 20),
                "pinterest": random.randint(0, 10)
            },
            "engagement_score": random.randint(50, 1000),
            "last_shared": datetime.utcnow().isoformat(),
            "most_shared_platform": "facebook"  # Would calculate based on data
        }
        
        return {
            "success": True,
            "data": stats
        }
        
    except Exception as e:
        logger.error(f"Error getting social stats for post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get social statistics")

@social_router.get("/analytics/overview")
async def get_social_analytics_overview(
    period: str = "30days",
    # current_user: User = Depends(require_role(UserRole.EDITOR))
):
    """Get overall social media analytics"""
    try:
        # Get analytics data
        platform_breakdown = get_platform_breakdown()
        engagement_trends = get_engagement_trends()
        
        analytics_data = {
            "period": period,
            "total_likes": sum([trend['likes'] for trend in engagement_trends]),
            "total_shares": sum([trend['shares'] for trend in engagement_trends]),
            "platform_breakdown": platform_breakdown,
            "engagement_trends": engagement_trends,
            "top_performing_platform": max(platform_breakdown, key=platform_breakdown.get),
            "average_engagement_per_day": round(
                sum([trend['engagement_score'] for trend in engagement_trends]) / len(engagement_trends), 2
            ) if engagement_trends else 0
        }
        
        return {
            "success": True,
            "data": analytics_data,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting social analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get social analytics")

@social_router.get("/top-posts")
async def get_top_social_posts(
    metric: str = "shares",  # 'likes', 'shares', or 'engagement'
    limit: int = 10,
    # current_user: User = Depends(get_current_active_user)
):
    """Get top performing posts by social media metrics"""
    try:
        if metric not in ['likes', 'shares', 'engagement']:
            raise HTTPException(status_code=400, detail="Metric must be 'likes', 'shares', or 'engagement'")
        
        # Mock top posts data
        import random
        
        top_posts = []
        for i in range(1, limit + 1):
            post = {
                "post_id": f"post_{i}",
                "title": f"Top Post #{i} - Amazing Content!",
                "likes": random.randint(50, 1000),
                "shares": random.randint(25, 500),
                "engagement_score": random.randint(100, 2000),
                "created_at": datetime.utcnow().isoformat(),
                "author": f"Author {i}",
                "top_platform": random.choice(['facebook', 'twitter', 'linkedin', 'whatsapp'])
            }
            top_posts.append(post)
        
        # Sort by requested metric
        if metric == 'likes':
            top_posts.sort(key=lambda x: x['likes'], reverse=True)
        elif metric == 'shares':
            top_posts.sort(key=lambda x: x['shares'], reverse=True)
        else:  # engagement
            top_posts.sort(key=lambda x: x['engagement_score'], reverse=True)
        
        return {
            "success": True,
            "metric": metric,
            "limit": limit,
            "data": top_posts
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting top posts: {e}")
        raise HTTPException(status_code=500, detail="Failed to get top posts")

@social_router.post("/bulk-share")
async def bulk_share_posts(
    bulk_data: Dict[str, Any] = Body(...),
    # current_user: User = Depends(require_role(UserRole.EDITOR))
):
    """Share multiple posts to social media at once"""
    try:
        post_ids = bulk_data.get('post_ids', [])
        platforms = bulk_data.get('platforms', [])
        custom_message = bulk_data.get('message', 'Check out these amazing posts!')
        
        if not post_ids:
            raise HTTPException(status_code=400, detail="Post IDs are required")
        
        if not platforms:
            raise HTTPException(status_code=400, detail="At least one platform is required")
        
        results = []
        
        for post_id in post_ids:
            for platform in platforms:
                try:
                    # Track each share
                    event_result = await track_share_event(post_id, platform, "current_user.id")
                    
                    results.append({
                        "post_id": post_id,
                        "platform": platform,
                        "success": True,
                        "event_id": event_result.get('event_id')
                    })
                    
                except Exception as e:
                    results.append({
                        "post_id": post_id,
                        "platform": platform,
                        "success": False,
                        "error": str(e)
                    })
        
        successful_shares = len([r for r in results if r['success']])
        total_attempts = len(results)
        
        return {
            "success": True,
            "message": f"Bulk share completed: {successful_shares}/{total_attempts} successful",
            "results": results,
            "summary": {
                "total_posts": len(post_ids),
                "total_platforms": len(platforms),
                "successful_shares": successful_shares,
                "failed_shares": total_attempts - successful_shares
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in bulk share: {e}")
        raise HTTPException(status_code=500, detail="Failed to complete bulk share")

@social_router.get("/share-urls/{post_id}")
async def get_share_urls(
    post_id: str,
    custom_message: str = "Check out this awesome post!",
    # current_user: User = Depends(get_current_active_user)
):
    """Get pre-generated share URLs for all platforms"""
    try:
        # This would typically get post data from database
        base_url = "https://your-cms-domain.com"  # Would be configured
        post_url = f"{base_url}/posts/{post_id}"
        
        share_urls = {
            'facebook': f"https://www.facebook.com/sharer/sharer.php?u={post_url}",
            'twitter': f"https://twitter.com/intent/tweet?text={custom_message}&url={post_url}",
            'linkedin': f"https://www.linkedin.com/sharing/share-offsite/?url={post_url}",
            'whatsapp': f"https://wa.me/?text={custom_message} {post_url}",
            'telegram': f"https://t.me/share/url?url={post_url}&text={custom_message}",
            'reddit': f"https://reddit.com/submit?url={post_url}&title={custom_message}",
            'pinterest': f"https://pinterest.com/pin/create/button/?url={post_url}&description={custom_message}"
        }
        
        return {
            "success": True,
            "post_id": post_id,
            "post_url": post_url,
            "share_urls": share_urls,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating share URLs: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate share URLs")
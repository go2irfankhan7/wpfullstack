# Backend hooks for Social Media Share & Like Plugin
from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

async def post_meta(data: Dict[str, Any]) -> Dict[str, Any]:
    """Add social media metadata to posts"""
    
    post_data = data.get('post', {})
    post_id = post_data.get('id')
    
    if not post_id:
        return data
    
    # Add social media metadata
    social_meta = {
        'likes': post_data.get('likes', 0),
        'shares': post_data.get('shares', 0),
        'share_platforms': {
            'facebook': post_data.get('facebook_shares', 0),
            'twitter': post_data.get('twitter_shares', 0),
            'linkedin': post_data.get('linkedin_shares', 0),
            'whatsapp': post_data.get('whatsapp_shares', 0),
            'telegram': post_data.get('telegram_shares', 0),
            'reddit': post_data.get('reddit_shares', 0),
            'pinterest': post_data.get('pinterest_shares', 0)
        },
        'last_shared': post_data.get('last_shared'),
        'most_shared_platform': get_most_shared_platform(post_data),
        'engagement_score': calculate_engagement_score(post_data)
    }
    
    return {
        **data,
        'social_meta': social_meta
    }

async def social_analytics(data: Dict[str, Any]) -> Dict[str, Any]:
    """Process social media analytics data"""
    
    try:
        # Get social engagement metrics
        analytics_data = {
            'total_likes': get_total_likes(),
            'total_shares': get_total_shares(),
            'top_shared_posts': get_top_shared_posts(limit=5),
            'platform_breakdown': get_platform_breakdown(),
            'engagement_trends': get_engagement_trends(),
            'viral_posts': get_viral_posts()
        }
        
        return {
            **data,
            'social_analytics': analytics_data
        }
        
    except Exception as e:
        logger.error(f"Error processing social analytics: {e}")
        return data

async def before_post_save(post_data: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize social media data for new posts"""
    
    # Initialize social media fields if not present
    if 'likes' not in post_data:
        post_data['likes'] = 0
    
    if 'shares' not in post_data:
        post_data['shares'] = 0
    
    if 'social_meta' not in post_data:
        post_data['social_meta'] = {
            'facebook_shares': 0,
            'twitter_shares': 0,
            'linkedin_shares': 0,
            'whatsapp_shares': 0,
            'telegram_shares': 0,
            'reddit_shares': 0,
            'pinterest_shares': 0,
            'created_at': datetime.utcnow().isoformat(),
            'share_urls': generate_share_urls(post_data)
        }
    
    return post_data

async def after_post_save(post_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update social media tracking after post save"""
    
    post_id = post_data.get('id')
    if not post_id:
        return post_data
    
    try:
        # Log post creation for social tracking
        social_event = {
            'event_type': 'post_created',
            'post_id': post_id,
            'post_title': post_data.get('title'),
            'timestamp': datetime.utcnow().isoformat(),
            'social_ready': True
        }
        
        # Here you would typically save to a social events table
        # or send to an analytics service
        logger.info(f"Social tracking initialized for post: {post_id}")
        
        return post_data
        
    except Exception as e:
        logger.error(f"Error setting up social tracking: {e}")
        return post_data

def generate_share_urls(post_data: Dict[str, Any]) -> Dict[str, str]:
    """Generate social media share URLs for a post"""
    
    post_id = post_data.get('id', 'new')
    post_title = post_data.get('title', 'Check out this post!')
    base_url = "https://your-cms-domain.com"  # Would be configured
    post_url = f"{base_url}/posts/{post_id}"
    
    share_text = f"Check out this awesome post: {post_title}"
    
    return {
        'facebook': f"https://www.facebook.com/sharer/sharer.php?u={post_url}",
        'twitter': f"https://twitter.com/intent/tweet?text={share_text}&url={post_url}",
        'linkedin': f"https://www.linkedin.com/sharing/share-offsite/?url={post_url}",
        'whatsapp': f"https://wa.me/?text={share_text} {post_url}",
        'telegram': f"https://t.me/share/url?url={post_url}&text={share_text}",
        'reddit': f"https://reddit.com/submit?url={post_url}&title={post_title}",
        'pinterest': f"https://pinterest.com/pin/create/button/?url={post_url}&description={share_text}"
    }

def get_most_shared_platform(post_data: Dict[str, Any]) -> str:
    """Get the platform where this post was shared most"""
    
    platforms = {
        'facebook': post_data.get('facebook_shares', 0),
        'twitter': post_data.get('twitter_shares', 0),
        'linkedin': post_data.get('linkedin_shares', 0),
        'whatsapp': post_data.get('whatsapp_shares', 0),
        'telegram': post_data.get('telegram_shares', 0),
        'reddit': post_data.get('reddit_shares', 0),
        'pinterest': post_data.get('pinterest_shares', 0)
    }
    
    if not any(platforms.values()):
        return 'none'
    
    return max(platforms, key=platforms.get)

def calculate_engagement_score(post_data: Dict[str, Any]) -> float:
    """Calculate engagement score based on likes and shares"""
    
    likes = post_data.get('likes', 0)
    total_shares = sum([
        post_data.get('facebook_shares', 0),
        post_data.get('twitter_shares', 0),
        post_data.get('linkedin_shares', 0),
        post_data.get('whatsapp_shares', 0),
        post_data.get('telegram_shares', 0),
        post_data.get('reddit_shares', 0),
        post_data.get('pinterest_shares', 0)
    ])
    
    # Weighted engagement score (shares worth more than likes)
    engagement_score = (likes * 1.0) + (total_shares * 2.5)
    
    return round(engagement_score, 2)

def get_total_likes() -> int:
    """Get total likes across all posts (mock implementation)"""
    # In a real implementation, this would query the database
    import random
    return random.randint(1000, 5000)

def get_total_shares() -> int:
    """Get total shares across all posts (mock implementation)"""
    import random
    return random.randint(500, 2000)

def get_top_shared_posts(limit: int = 5) -> List[Dict[str, Any]]:
    """Get most shared posts (mock implementation)"""
    import random
    
    # Mock data - in real implementation, would query database
    return [
        {
            'post_id': f'post_{i}',
            'title': f'Popular Post #{i}',
            'shares': random.randint(50, 200),
            'likes': random.randint(100, 500),
            'engagement_score': random.randint(200, 800)
        }
        for i in range(1, limit + 1)
    ]

def get_platform_breakdown() -> Dict[str, int]:
    """Get share breakdown by platform (mock implementation)"""
    import random
    
    return {
        'facebook': random.randint(100, 300),
        'twitter': random.randint(80, 250),
        'linkedin': random.randint(50, 150),
        'whatsapp': random.randint(70, 200),
        'telegram': random.randint(20, 80),
        'reddit': random.randint(30, 100),
        'pinterest': random.randint(15, 60)
    }

def get_engagement_trends() -> List[Dict[str, Any]]:
    """Get engagement trends over time (mock implementation)"""
    from datetime import datetime, timedelta
    import random
    
    trends = []
    for i in range(7):  # Last 7 days
        date = datetime.utcnow() - timedelta(days=i)
        trends.append({
            'date': date.strftime('%Y-%m-%d'),
            'likes': random.randint(50, 200),
            'shares': random.randint(20, 100),
            'engagement_score': random.randint(100, 500)
        })
    
    return list(reversed(trends))

def get_viral_posts(threshold: int = 100) -> List[Dict[str, Any]]:
    """Get posts that went viral (high share count)"""
    import random
    
    # Mock viral posts
    return [
        {
            'post_id': 'viral_1',
            'title': 'This Post Went Viral!',
            'shares': random.randint(300, 1000),
            'likes': random.randint(500, 2000),
            'viral_date': (datetime.utcnow() - timedelta(days=2)).isoformat(),
            'top_platform': 'twitter'
        },
        {
            'post_id': 'viral_2', 
            'title': 'Another Viral Hit',
            'shares': random.randint(200, 800),
            'likes': random.randint(400, 1500),
            'viral_date': (datetime.utcnow() - timedelta(days=5)).isoformat(),
            'top_platform': 'facebook'
        }
    ]

# Social media event tracking functions
async def track_like_event(post_id: str, user_id: str, action: str) -> Dict[str, Any]:
    """Track like/unlike events"""
    
    event_data = {
        'event_type': 'like' if action == 'like' else 'unlike',
        'post_id': post_id,
        'user_id': user_id,
        'timestamp': datetime.utcnow().isoformat(),
        'ip_address': 'user_ip_here',  # Would get from request
        'user_agent': 'user_agent_here'  # Would get from request
    }
    
    # Here you would save to database
    logger.info(f"Tracked {action} event for post {post_id} by user {user_id}")
    
    return {
        'success': True,
        'event_id': f"evt_{int(datetime.utcnow().timestamp())}",
        'event_data': event_data
    }

async def track_share_event(post_id: str, platform: str, user_id: str = None) -> Dict[str, Any]:
    """Track social media share events"""
    
    event_data = {
        'event_type': 'share',
        'post_id': post_id,
        'platform': platform,
        'user_id': user_id,
        'timestamp': datetime.utcnow().isoformat(),
        'referrer': 'social_share_plugin'
    }
    
    # Here you would save to database and increment counters
    logger.info(f"Tracked share event for post {post_id} on {platform}")
    
    return {
        'success': True,
        'event_id': f"share_{int(datetime.utcnow().timestamp())}",
        'event_data': event_data
    }
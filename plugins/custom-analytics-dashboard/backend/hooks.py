# Backend hooks for Custom Analytics Plugin
from datetime import datetime, timedelta
import random
from typing import Dict, Any

async def dashboard_stats(data: Dict[str, Any]) -> Dict[str, Any]:
    """Add custom analytics stats to dashboard"""
    
    # Simulate analytics data (replace with real analytics logic)
    page_views = random.randint(10000, 15000)
    unique_visitors = random.randint(2000, 4000)
    bounce_rate = f"{random.randint(25, 40)}%"
    
    # Add custom stats
    custom_stats = data.get('stats', {})
    custom_stats.update({
        'page_views': page_views,
        'unique_visitors': unique_visitors,
        'bounce_rate': bounce_rate,
        'analytics_enabled': True
    })
    
    # Add analytics activity
    analytics_activity = {
        'type': 'analytics',
        'title': f'Analytics Update: {page_views:,} page views today',
        'description': f'Traffic increased by {random.randint(5, 25)}% compared to yesterday',
        'timestamp': datetime.utcnow().isoformat(),
        'icon': 'TrendingUp'
    }
    
    recent_activity = data.get('recent_activity', [])
    recent_activity.insert(0, analytics_activity)
    
    return {
        **data,
        'stats': custom_stats,
        'recent_activity': recent_activity
    }

async def before_post_save(post_data: Dict[str, Any]) -> Dict[str, Any]:
    """Track post analytics before saving"""
    
    # Add analytics tracking metadata
    post_data['analytics'] = {
        'tracked': True,
        'tracking_id': f"post_{post_data.get('id', 'new')}_{int(datetime.utcnow().timestamp())}",
        'created_at': datetime.utcnow().isoformat()
    }
    
    return post_data

async def after_post_save(post_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update analytics after post is saved"""
    
    # Here you would typically:
    # 1. Log the post creation/update event
    # 2. Update analytics counters
    # 3. Send notifications to analytics services
    
    print(f"Analytics: Post '{post_data.get('title')}' was saved with tracking ID: {post_data.get('analytics', {}).get('tracking_id')}")
    
    return post_data

def get_analytics_data(period: str = '30days') -> Dict[str, Any]:
    """Get analytics data for specified period"""
    
    # Simulate analytics data generation
    end_date = datetime.utcnow()
    
    if period == '7days':
        start_date = end_date - timedelta(days=7)
        multiplier = 1
    elif period == '90days':
        start_date = end_date - timedelta(days=90)
        multiplier = 3
    else:  # 30days default
        start_date = end_date - timedelta(days=30)
        multiplier = 2
    
    return {
        'period': period,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'total_page_views': random.randint(50000, 100000) * multiplier,
        'unique_visitors': random.randint(10000, 25000) * multiplier,
        'bounce_rate': f"{random.randint(25, 45)}%",
        'top_pages': [
            {'path': '/', 'views': random.randint(5000, 10000)},
            {'path': '/blog', 'views': random.randint(2000, 5000)},
            {'path': '/about', 'views': random.randint(1000, 3000)},
            {'path': '/contact', 'views': random.randint(500, 1500)}
        ],
        'traffic_sources': {
            'direct': f"{random.randint(30, 50)}%",
            'search': f"{random.randint(25, 40)}%", 
            'social': f"{random.randint(10, 20)}%",
            'referral': f"{random.randint(5, 15)}%"
        }
    }
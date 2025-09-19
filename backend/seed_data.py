import asyncio
from datetime import datetime
from auth import get_password_hash
from database import insert_document, find_document
from models import UserRole, ContentStatus, PluginStatus
import logging

logger = logging.getLogger(__name__)

async def seed_database():
    """Seed the database with initial data"""
    try:
        await seed_users()
        await seed_posts()
        await seed_pages()
        await seed_plugins()
        await seed_settings()
        logger.info("Database seeded successfully")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")

async def seed_users():
    """Seed initial users"""
    users = [
        {
            "_id": "admin-user-001",
            "name": "Admin User",
            "email": "admin@cms.com",
            "password_hash": get_password_hash("admin123"),
            "role": UserRole.ADMIN,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=admin",
            "is_active": True
        },
        {
            "_id": "editor-user-001",
            "name": "Editor User",
            "email": "editor@cms.com",
            "password_hash": get_password_hash("editor123"),
            "role": UserRole.EDITOR,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=editor",
            "is_active": True
        },
        {
            "_id": "author-user-001",
            "name": "Author User",
            "email": "author@cms.com",
            "password_hash": get_password_hash("author123"),
            "role": UserRole.AUTHOR,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=author",
            "is_active": True
        }
    ]
    
    for user_data in users:
        existing_user = await find_document("users", {"email": user_data["email"]})
        if not existing_user:
            await insert_document("users", user_data)
            logger.info(f"Seeded user: {user_data['email']}")

async def seed_posts():
    """Seed initial posts"""
    posts = [
        {
            "_id": "welcome-post-001",
            "title": "Welcome to Our CMS",
            "content": "This is the first post in our new CMS system. It demonstrates the post creation and management functionality with full plugin support.",
            "excerpt": "A welcome post showcasing CMS functionality",
            "status": ContentStatus.PUBLISHED,
            "author_id": "admin-user-001",
            "featured_image": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=800&h=400&fit=crop",
            "tags": ["cms", "welcome", "first-post"],
            "category": "General"
        },
        {
            "_id": "plugin-architecture-001",
            "title": "Building with Plugins",
            "content": "Our CMS supports a powerful plugin architecture that allows extending functionality both on frontend and backend. This revolutionary system makes it possible to create WordPress-level extensibility with modern development practices.",
            "excerpt": "Learn about our revolutionary plugin system",
            "status": ContentStatus.PUBLISHED,
            "author_id": "editor-user-001",
            "featured_image": "https://images.unsplash.com/photo-1558655146-d09347e92766?w=800&h=400&fit=crop",
            "tags": ["plugins", "development", "architecture"],
            "category": "Development"
        }
    ]
    
    for post_data in posts:
        existing_post = await find_document("posts", {"_id": post_data["_id"]})
        if not existing_post:
            await insert_document("posts", post_data)
            logger.info(f"Seeded post: {post_data['title']}")

async def seed_pages():
    """Seed initial pages"""
    pages = [
        {
            "_id": "about-page-001",
            "title": "About Us",
            "content": "Learn more about our company and mission. We are building the next generation CMS platform with revolutionary plugin architecture.",
            "slug": "about-us",
            "status": ContentStatus.PUBLISHED,
            "author_id": "admin-user-001",
            "template": "default"
        },
        {
            "_id": "contact-page-001",
            "title": "Contact",
            "content": "Get in touch with us through our contact form or email. We'd love to hear from you!",
            "slug": "contact",
            "status": ContentStatus.DRAFT,
            "author_id": "editor-user-001",
            "template": "contact"
        }
    ]
    
    for page_data in pages:
        existing_page = await find_document("pages", {"_id": page_data["_id"]})
        if not existing_page:
            await insert_document("pages", page_data)
            logger.info(f"Seeded page: {page_data['title']}")

async def seed_plugins():
    """Seed initial plugins"""
    plugins = [
        {
            "_id": "contact-form-7",
            "name": "Contact Form 7",
            "description": "Simple yet flexible contact form plugin with spam protection and multiple form support.",
            "version": "1.0.0",
            "author": "CMS Team",
            "category": "Forms",
            "status": PluginStatus.AVAILABLE,
            "price": "Free",
            "icon": "https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?w=100&h=100&fit=crop",
            "screenshots": ["https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?w=600&h=400&fit=crop"],
            "features": [
                "Drag & drop form builder",
                "Spam protection",
                "Email notifications",
                "Custom styling options"
            ],
            "hooks": {
                "admin_menu": {
                    "type": "frontend",
                    "description": "Add Contact Forms menu item"
                },
                "post_content": {
                    "type": "frontend",
                    "description": "Process contact form shortcodes"
                }
            },
            "settings_schema": {
                "spam_protection": {"type": "boolean", "default": True},
                "notification_email": {"type": "string", "default": ""}
            }
        },
        {
            "_id": "seo-optimizer",
            "name": "SEO Optimizer",
            "description": "Complete SEO solution with meta tags, sitemap generation, and search engine optimization tools.",
            "version": "2.1.0",
            "author": "SEO Experts",
            "category": "SEO",
            "status": PluginStatus.AVAILABLE,
            "price": "$29",
            "icon": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=100&h=100&fit=crop",
            "screenshots": ["https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=400&fit=crop"],
            "features": [
                "Meta tag optimization",
                "XML sitemap generation",
                "Social media integration",
                "Analytics tracking"
            ],
            "hooks": {
                "admin_menu": {
                    "type": "frontend",
                    "description": "Add SEO Settings menu item"
                },
                "before_post_save": {
                    "type": "backend",
                    "description": "Optimize post SEO before saving"
                }
            }
        },
        {
            "_id": "ecommerce-lite",
            "name": "E-commerce Lite",
            "description": "Turn your CMS into an online store with products, shopping cart, and payment integration.",
            "version": "1.5.0",
            "author": "Commerce Team",
            "category": "E-commerce",
            "status": PluginStatus.AVAILABLE,
            "price": "$99",
            "icon": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=100&h=100&fit=crop",
            "screenshots": ["https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=600&h=400&fit=crop"],
            "features": [
                "Product management",
                "Shopping cart",
                "Payment gateway integration",
                "Order management"
            ],
            "hooks": {
                "admin_menu": {
                    "type": "frontend",
                    "description": "Add Products menu item"
                },
                "custom_endpoints": {
                    "type": "backend",
                    "description": "Add e-commerce API endpoints"
                }
            }
        },
        {
            "_id": "backup-manager",
            "name": "Backup Manager",
            "description": "Automated backup solution for your content, database, and files with cloud storage support.",
            "version": "1.2.0",
            "author": "Backup Solutions",
            "category": "Utility",
            "status": PluginStatus.AVAILABLE,
            "price": "Free",
            "icon": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=100&h=100&fit=crop",
            "screenshots": ["https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&h=400&fit=crop"],
            "features": [
                "Scheduled backups",
                "Cloud storage integration",
                "One-click restore",
                "Backup verification"
            ],
            "hooks": {
                "admin_menu": {
                    "type": "frontend",
                    "description": "Add Backups menu item"
                },
                "scheduled_tasks": {
                    "type": "backend",
                    "description": "Run automated backups"
                }
            }
        }
    ]
    
    for plugin_data in plugins:
        existing_plugin = await find_document("plugins", {"_id": plugin_data["_id"]})
        if not existing_plugin:
            await insert_document("plugins", plugin_data)
            logger.info(f"Seeded plugin: {plugin_data['name']}")

async def seed_settings():
    """Seed initial settings"""
    settings_data = {
        "_id": "site-settings-001",
        "site_name": "CMS Pro",
        "site_description": "A powerful plugin-based content management system",
        "site_url": "https://example.com",
        "timezone": "UTC",
        "date_format": "YYYY-MM-DD",
        "time_format": "24h",
        "email_notifications": True,
        "two_factor_auth": False,
        "cache_enabled": True
    }
    
    existing_settings = await find_document("settings", {"_id": settings_data["_id"]})
    if not existing_settings:
        await insert_document("settings", settings_data)
        logger.info("Seeded initial settings")

if __name__ == "__main__":
    asyncio.run(seed_database())
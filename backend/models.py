from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    AUTHOR = "author"

class ContentStatus(str, Enum):
    PUBLISHED = "published"
    DRAFT = "draft"
    PRIVATE = "private"

class PluginStatus(str, Enum):
    AVAILABLE = "available"
    INSTALLED = "installed"
    ACTIVE = "active"

# Base Models
class BaseDBModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}

# User Models
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.AUTHOR

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    avatar: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseDBModel):
    name: str
    email: str
    password_hash: str
    role: UserRole
    avatar: Optional[str] = None
    is_active: bool = True

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: UserRole
    avatar: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

# Content Models
class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str
    excerpt: Optional[str] = None
    status: ContentStatus = ContentStatus.DRAFT
    featured_image: Optional[str] = None
    tags: List[str] = []
    category: Optional[str] = None

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    excerpt: Optional[str] = None
    status: Optional[ContentStatus] = None
    featured_image: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None

class Post(BaseDBModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    status: ContentStatus
    author_id: str
    featured_image: Optional[str] = None
    tags: List[str] = []
    category: Optional[str] = None

class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    excerpt: Optional[str] = None
    status: ContentStatus
    author_id: str
    author: Optional[str] = None  # Populated from user lookup
    featured_image: Optional[str] = None
    tags: List[str] = []
    category: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class PageCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str
    slug: Optional[str] = None
    status: ContentStatus = ContentStatus.DRAFT
    template: str = "default"

class PageUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[ContentStatus] = None
    template: Optional[str] = None

class Page(BaseDBModel):
    title: str
    content: str
    slug: str
    status: ContentStatus
    author_id: str
    template: str = "default"

class PageResponse(BaseModel):
    id: str
    title: str
    content: str
    slug: str
    status: ContentStatus
    author_id: str
    author: Optional[str] = None  # Populated from user lookup
    template: str
    created_at: datetime
    updated_at: datetime

# Plugin Models
class PluginHookDefinition(BaseModel):
    name: str
    type: str  # frontend, backend, or both
    description: str
    execution_order: int = 10

class PluginMetadata(BaseModel):
    name: str
    description: str
    version: str
    author: str
    category: str
    price: str = "Free"
    features: List[str] = []
    dependencies: List[str] = []
    hooks: Dict[str, Any] = {}
    settings_schema: Dict[str, Any] = {}

class PluginCreate(BaseModel):
    metadata: PluginMetadata
    download_url: Optional[str] = None
    icon: Optional[str] = None
    screenshots: List[str] = []

class PluginUpdate(BaseModel):
    status: Optional[PluginStatus] = None
    settings: Optional[Dict[str, Any]] = None

class Plugin(BaseDBModel):
    name: str
    description: str
    version: str
    author: str
    category: str
    status: PluginStatus
    price: str = "Free"
    download_url: Optional[str] = None
    icon: Optional[str] = None
    screenshots: List[str] = []
    features: List[str] = []
    dependencies: List[str] = []
    hooks: Dict[str, Any] = {}
    settings_schema: Dict[str, Any] = {}
    settings: Dict[str, Any] = {}
    install_path: Optional[str] = None

class PluginResponse(BaseModel):
    id: str
    name: str
    description: str
    version: str
    author: str
    category: str
    status: PluginStatus
    price: str
    download_url: Optional[str] = None
    icon: Optional[str] = None
    screenshots: List[str] = []
    features: List[str] = []
    dependencies: List[str] = []
    hooks: Dict[str, Any] = {}
    settings_schema: Dict[str, Any] = {}
    settings: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

# Plugin Hook Execution Models
class PluginHookExecution(BaseModel):
    plugin_id: str
    hook_name: str
    data: Dict[str, Any] = {}

class PluginHookResult(BaseModel):
    plugin_id: str
    hook_name: str
    result: Any
    success: bool
    error: Optional[str] = None

# Authentication Models
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    user_id: Optional[str] = None

# Media Models
class MediaUpload(BaseModel):
    filename: str
    content_type: str
    size: int

class MediaResponse(BaseModel):
    id: str
    filename: str
    original_name: str
    content_type: str
    size: int
    url: str
    uploaded_by: str
    created_at: datetime

# Settings Models
class SettingsUpdate(BaseModel):
    site_name: Optional[str] = None
    site_description: Optional[str] = None
    site_url: Optional[str] = None
    timezone: Optional[str] = None
    date_format: Optional[str] = None
    time_format: Optional[str] = None
    email_notifications: Optional[bool] = None
    two_factor_auth: Optional[bool] = None
    cache_enabled: Optional[bool] = None

class Settings(BaseDBModel):
    site_name: str = "CMS Pro"
    site_description: str = "A powerful plugin-based content management system"
    site_url: str = "https://example.com"
    timezone: str = "UTC"
    date_format: str = "YYYY-MM-DD"
    time_format: str = "24h"
    email_notifications: bool = True
    two_factor_auth: bool = False
    cache_enabled: bool = True

# Dashboard Models
class DashboardStats(BaseModel):
    total_posts: int
    total_pages: int
    total_users: int
    active_plugins: int
    recent_activity: List[Dict[str, Any]] = []
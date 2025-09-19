# CMS Pro - Backend Integration Contracts

## Overview
This document outlines the API contracts, data models, and integration strategy for transforming the current frontend-only CMS into a full-stack application with plugin architecture.

## Current Mock Data Structure

### Users
- Authentication system with role-based access (admin, editor, author)
- User profiles with avatars and permissions
- Session management and security features

### Posts & Pages
- Content management with WYSIWYG editing capabilities
- Status management (published, draft, private)
- Media attachments and featured images
- Category and tag system
- Author attribution and timestamps

### Plugin System (Core Innovation)
- Plugin marketplace with installation/activation
- Hook-based architecture for extending functionality
- Plugin metadata and version management
- Runtime plugin execution and dependency management

## API Contracts

### Authentication Endpoints
```
POST /api/auth/login
POST /api/auth/logout  
POST /api/auth/refresh
GET /api/auth/me
```

### User Management
```
GET /api/users
POST /api/users
GET /api/users/{id}
PUT /api/users/{id}
DELETE /api/users/{id}
PUT /api/users/{id}/role
```

### Content Management
```
GET /api/posts
POST /api/posts
GET /api/posts/{id}
PUT /api/posts/{id}
DELETE /api/posts/{id}
PUT /api/posts/{id}/status

GET /api/pages
POST /api/pages
GET /api/pages/{id}
PUT /api/pages/{id}
DELETE /api/pages/{id}
```

### Plugin System (Revolutionary Feature)
```
GET /api/plugins                    # List all available plugins
POST /api/plugins/install          # Install a plugin
PUT /api/plugins/{id}/activate     # Activate plugin
PUT /api/plugins/{id}/deactivate   # Deactivate plugin
DELETE /api/plugins/{id}           # Uninstall plugin
GET /api/plugins/{id}/settings     # Get plugin settings
PUT /api/plugins/{id}/settings     # Update plugin settings
POST /api/plugins/execute-hook     # Execute plugin hooks
```

### Media Management
```
POST /api/media/upload
GET /api/media
DELETE /api/media/{id}
```

## Database Models

### Plugin Model (Core Innovation)
```python
class Plugin:
    id: str
    name: str
    description: str
    version: str
    author: str
    category: str
    status: str (available, installed, active)
    metadata: dict
    hooks: dict  # Frontend and backend hook definitions
    dependencies: list
    settings_schema: dict
    install_path: str
    created_at: datetime
    updated_at: datetime
```

### PluginHook Model
```python
class PluginHook:
    id: str
    plugin_id: str
    hook_name: str
    hook_type: str  # frontend, backend, or both
    execution_order: int
    is_active: bool
```

### User Model
```python
class User:
    id: str
    name: str
    email: str
    password_hash: str
    role: str  # admin, editor, author
    avatar: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

### Post/Page Models
```python
class Post:
    id: str
    title: str
    content: str
    excerpt: str
    status: str  # published, draft, private
    author_id: str
    featured_image: str
    tags: list
    category: str
    created_at: datetime
    updated_at: datetime

class Page:
    id: str
    title: str
    content: str
    slug: str
    status: str
    author_id: str
    template: str
    created_at: datetime
    updated_at: datetime
```

## Plugin Architecture Implementation

### Plugin Hook System
The revolutionary feature of this CMS is its dual-sided plugin system:

1. **Frontend Hooks**: React components and context modifications
   - `admin_menu`: Add menu items to admin sidebar
   - `post_content`: Modify post content rendering
   - `admin_layout`: Modify admin layout
   - `dashboard_stats`: Add custom dashboard widgets

2. **Backend Hooks**: API extensions and business logic
   - `before_post_save`: Pre-processing before saving posts
   - `after_post_save`: Post-processing after saving posts
   - `custom_endpoints`: Add new API endpoints
   - `authentication`: Custom authentication logic

### Plugin Installation Flow
1. Plugin uploaded as ZIP file containing:
   - `plugin.json`: Metadata and hook definitions
   - `frontend/`: React components and hooks
   - `backend/`: Python modules and API endpoints
   - `migrations/`: Database schema changes

2. Server extracts and validates plugin structure
3. Database migrations are applied
4. Plugin hooks are registered in the system
5. Plugin becomes available for activation

### Security Considerations
- Plugin sandboxing to prevent malicious code
- Permission-based plugin installation (admin only)
- Code review system for public plugins
- Plugin signature verification

## Frontend Integration Changes

### Remove Mock Data
Replace all instances in:
- `src/contexts/AuthContext.js`
- `src/contexts/PluginContext.js`
- `src/pages/*.js`

### Add API Integration
- Implement axios interceptors for authentication
- Add loading states and error handling
- Implement real-time updates for plugin activation
- Add form validation and submission handlers

### Plugin System Frontend Updates
- Dynamic menu item registration from active plugins
- Plugin-contributed dashboard widgets
- Real-time plugin activation/deactivation
- Plugin settings management interface

## Backend Implementation Priority

1. **Phase 1**: Core CMS functionality
   - User authentication and authorization
   - Basic CRUD for posts/pages
   - File upload system

2. **Phase 2**: Plugin Infrastructure (Revolutionary)
   - Plugin model and database schema
   - Plugin installation and management system
   - Hook execution engine
   - Plugin sandbox environment

3. **Phase 3**: Advanced Features
   - Real-time notifications
   - Advanced search and filtering
   - Backup and restore functionality
   - Multi-site management

## Security & Performance

### Authentication
- JWT tokens with refresh mechanism
- Role-based access control
- Session management
- Password hashing with bcrypt

### Plugin Security
- Code scanning for malicious patterns
- Isolated execution environment
- Permission system for plugin capabilities
- Audit logging for plugin actions

### Performance Optimization
- Database indexing for queries
- Caching layer for plugin hooks
- Lazy loading for plugin components
- CDN integration for media files

## Testing Strategy

### Backend Testing
- Unit tests for all API endpoints
- Plugin system integration tests
- Security vulnerability scanning
- Performance benchmarking

### Frontend Testing
- Component testing with React Testing Library
- Plugin integration testing
- User workflow testing
- Cross-browser compatibility

This contracts document serves as the blueprint for building a truly innovative CMS with a plugin-first architecture that can compete with WordPress while offering modern development practices and superior extensibility.
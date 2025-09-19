# Custom Analytics Dashboard Plugin

## Description
Advanced analytics dashboard plugin for CMS Pro that provides comprehensive visitor tracking, traffic analytics, and detailed reporting capabilities.

## Features
- ✨ Real-time visitor tracking
- 📊 Custom dashboard widgets  
- 📈 Traffic analytics and trends
- 🎯 Performance metrics
- 📋 Exportable reports
- 🔧 Configurable settings
- 🌍 Geographic visitor data
- 📱 Mobile-responsive charts

## Installation
1. Download the plugin ZIP file
2. Go to Admin → Plugins in your CMS Pro dashboard
3. Click "Upload Plugin" 
4. Select the ZIP file and upload
5. Activate the plugin from the plugins list

## Configuration
After activation, configure the plugin:

1. Go to Admin → Plugins → Custom Analytics → Settings
2. Enable visitor tracking
3. Set your preferred analytics period (7, 30, or 90 days)
4. Add your analytics API key if using external services

## Usage

### Dashboard Integration
The plugin automatically adds analytics widgets to your main dashboard showing:
- Page views
- Unique visitors  
- Bounce rate
- Average session duration

### Analytics Dashboard
Access the full analytics dashboard via Admin → Analytics:
- Detailed traffic reports
- Visitor demographics
- Top performing pages
- Traffic source breakdown

### API Endpoints
The plugin adds these API endpoints:
- `GET /api/analytics/stats` - Get analytics statistics
- `GET /api/analytics/traffic` - Get traffic data  
- `POST /api/analytics/track-event` - Track custom events
- `GET /api/analytics/reports/export` - Export reports

## Hooks Used
This plugin demonstrates both frontend and backend hooks:

**Frontend Hooks:**
- `admin_menu` - Adds Analytics menu item
- `dashboard_stats` - Adds custom dashboard widgets

**Backend Hooks:**  
- `dashboard_stats` - Provides analytics data
- `before_post_save` - Tracks post analytics
- `after_post_save` - Updates analytics counters

## Development
To modify this plugin:
1. Edit the hooks in `frontend/hooks.js` and `backend/hooks.py`
2. Add new endpoints in `backend/endpoints.py`
3. Update settings schema in `plugin.json`
4. Repackage as ZIP and reinstall

## Version History
- **1.0.0** - Initial release with core analytics features

## Support
For support or feature requests, please contact the plugin developer.

## License
MIT License - Free to use and modify.
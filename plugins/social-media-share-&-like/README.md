# Social Media Share & Like Plugin

## Description
A comprehensive social media integration plugin for CMS Pro that adds beautiful share buttons, like functionality, and detailed social analytics to your posts. Transform your content into viral-ready social media posts with just one click!

## ✨ Features

### 🚀 Social Sharing
- **7 Major Platforms**: Facebook, Twitter, LinkedIn, WhatsApp, Telegram, Reddit, Pinterest
- **Smart Share URLs**: Pre-generated optimized sharing links
- **Custom Messages**: Personalized share text for each post
- **Share Tracking**: Monitor which platforms drive the most engagement
- **Bulk Sharing**: Share multiple posts across platforms simultaneously

### ❤️ Like System
- **Internal Likes**: Built-in like system for your posts
- **Real-time Updates**: Instant like count updates
- **User Tracking**: Track which users liked which posts
- **Like Analytics**: Monitor like trends and popular content

### 📊 Analytics & Insights
- **Engagement Metrics**: Track likes, shares, and overall engagement
- **Platform Breakdown**: See which social platforms perform best
- **Viral Detection**: Identify posts that are trending
- **Engagement Trends**: Monitor social media performance over time
- **Top Posts**: Discover your most engaging content

### 🎨 Customization
- **Multiple Styles**: Rounded, square, or circular buttons
- **Size Options**: Small, medium, or large button sizes
- **Positioning**: Top, bottom, both, or floating placement
- **Color Themes**: Match your brand colors
- **Mobile Responsive**: Perfect on all devices

## 🛠️ Installation

1. **Download**: Get the plugin ZIP file
2. **Upload**: Go to Admin → Plugins → Upload Plugin
3. **Install**: Select the ZIP file and click Install
4. **Activate**: Enable the plugin from the plugins list
5. **Configure**: Set up your preferences in Admin → Social Share

## ⚙️ Configuration

### Social Platforms
Choose which social media platforms to enable:
- ✅ Facebook - World's largest social network
- ✅ Twitter - Real-time news and updates
- ✅ LinkedIn - Professional networking
- ✅ WhatsApp - Private messaging and groups
- ✅ Telegram - Secure messaging platform
- ✅ Reddit - Community discussions
- ✅ Pinterest - Visual discovery platform

### Appearance Settings
- **Button Style**: Choose from rounded, square, or circular designs
- **Button Size**: Select small, medium, or large sizes
- **Position**: Place buttons at top, bottom, both, or floating
- **Colors**: Customize to match your brand (Pro feature)

### Feature Controls
- **Like Button**: Enable/disable internal like system
- **Share Count**: Show/hide share statistics
- **Custom Messages**: Set default share text per platform
- **Analytics**: Track engagement and social performance

## 🔧 Usage

### Automatic Integration
Once activated, social share buttons automatically appear on all your posts based on your position settings. No additional setup required!

### Manual Integration
For custom placement, use the shortcode in your content:
```
[social-share post-id="123" style="rounded" size="medium"]
```

### API Endpoints
The plugin adds these API endpoints for advanced usage:

#### Like System
```javascript
// Like a post
POST /api/social/posts/{post_id}/like
{
  "action": "like" // or "unlike"
}

// Get post social stats
GET /api/social/posts/{post_id}/stats
```

#### Share Tracking
```javascript
// Track a share
POST /api/social/posts/{post_id}/share
{
  "platform": "facebook"
}

// Get share URLs
GET /api/social/share-urls/{post_id}
```

#### Analytics
```javascript
// Get social analytics
GET /api/social/analytics/overview?period=30days

// Get top posts by engagement
GET /api/social/top-posts?metric=engagement&limit=10
```

## 📈 Analytics Dashboard

Access comprehensive social media analytics through **Admin → Social Share**:

### Overview Metrics
- Total likes across all posts
- Total shares by platform
- Engagement trends over time
- Top performing content

### Post Performance
- Individual post analytics
- Platform-specific share counts
- Engagement scores and rankings
- Viral post detection

### Platform Insights
- Which platforms drive the most traffic
- Optimal posting times for each platform
- Audience engagement patterns
- Growth trends and opportunities

## 🎯 Hook Integration

This plugin demonstrates advanced hook usage:

### Frontend Hooks
```javascript
// Add menu item
admin_menu(menuItems) {
  return [...menuItems, {
    title: 'Social Share',
    path: '/admin/social-share'
  }];
}

// Modify post content
post_content(data) {
  // Automatically add share buttons to posts
  return modifiedContent;
}
```

### Backend Hooks
```python
# Track social metadata
async def post_meta(data):
    # Add social engagement data
    return enhanced_data

# Analytics processing
async def social_analytics(data):
    # Process social media metrics
    return analytics_data
```

## 🚀 Advanced Features

### Viral Detection
Automatically identifies posts that are gaining viral traction based on:
- Share velocity (shares per hour)
- Cross-platform engagement
- Engagement rate vs. typical performance
- Social media mentions and backlinks

### Smart Scheduling
- Optimal posting time suggestions
- Platform-specific timing recommendations
- Engagement pattern analysis
- Automated social media posting (Pro feature)

### Integration Ready
- Google Analytics integration
- Facebook Pixel tracking
- Twitter Analytics sync
- Custom webhook support

## 🔒 Privacy & Security

- **No External Tracking**: All data stays in your CMS
- **GDPR Compliant**: Full user privacy protection
- **Secure APIs**: Authenticated endpoint access
- **Data Encryption**: Sensitive analytics data encrypted
- **User Consent**: Optional consent management

## 📱 Mobile Optimization

- **Responsive Design**: Perfect on all screen sizes
- **Touch Friendly**: Large, easy-to-tap buttons
- **Native Sharing**: Uses device's native share when available
- **Fast Loading**: Optimized for mobile networks
- **Offline Support**: Cached sharing options

## 🎨 Customization Examples

### Custom CSS
```css
.social-share-plugin .share-button {
  background: your-brand-color;
  border-radius: 15px;
  transition: all 0.3s ease;
}
```

### JavaScript Hooks
```javascript
// Custom share tracking
document.addEventListener('socialShare', function(event) {
  // Your custom analytics code
  gtag('event', 'share', {
    platform: event.detail.platform,
    post_id: event.detail.postId
  });
});
```

## 🔄 Updates & Changelog

### Version 1.0.0
- ✨ Initial release
- 🎯 7 major social platforms
- 📊 Complete analytics dashboard
- ❤️ Built-in like system
- 🎨 3 button styles and sizes
- 📱 Mobile-responsive design

### Planned Features
- 🤖 AI-powered share text optimization
- 📅 Scheduled social media posting
- 🎨 Advanced visual customization
- 🔗 Social media account integration
- 📈 A/B testing for share buttons

## 🆘 Support & Documentation

### Getting Help
- 📖 Full documentation: `/admin/social-share/docs`
- 💬 Community forum: Link to your support forum
- 📧 Direct support: your-support-email
- 🐛 Bug reports: GitHub issues or support system

### Troubleshooting
- **Buttons not showing**: Check plugin activation and position settings
- **Share counts not updating**: Verify API connectivity and authentication
- **Style issues**: Check for CSS conflicts with your theme
- **Analytics not loading**: Confirm user permissions and data availability

## 📄 License

MIT License - Free to use, modify, and distribute. Commercial usage allowed.

## 🙏 Credits

Built with love for the CMS Pro community. Special thanks to:
- Lucide React for beautiful icons
- Social media platforms for their sharing APIs
- The CMS Pro plugin system architecture
- Community feedback and feature requests

---

**Transform your content into social media gold! 🚀✨**
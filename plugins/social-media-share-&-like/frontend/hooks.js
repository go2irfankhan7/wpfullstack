// Frontend hooks for Social Media Share & Like Plugin
import React, { useState, useEffect } from 'react';
import { Share2, Heart, Facebook, Twitter, Linkedin, MessageCircle, Send, Hash, Image } from 'lucide-react';

// Hook to add Social Share menu item to admin sidebar
export function admin_menu(menuItems) {
  return [
    ...menuItems,
    {
      title: 'Social Share',
      path: '/admin/social-share',
      icon: Share2,
      roles: ['admin', 'editor']
    }
  ];
}

// Hook to add social share buttons to post content
export function post_content(data) {
  const { content, post } = data;
  
  if (!post || !content) return data;
  
  // Get plugin settings (would normally come from backend)
  const settings = {
    enabled_platforms: ['facebook', 'twitter', 'linkedin', 'whatsapp'],
    button_style: 'rounded',
    button_size: 'medium',
    position: 'bottom',
    show_share_count: true,
    show_like_button: true,
    custom_message: 'Check out this awesome post!'
  };
  
  const socialShareButtons = <SocialShareButtons post={post} settings={settings} />;
  
  // Add social share buttons based on position setting
  let modifiedContent = content;
  
  if (settings.position === 'top' || settings.position === 'both') {
    modifiedContent = (
      <>
        {socialShareButtons}
        <div className="mt-4">{content}</div>
      </>
    );
  }
  
  if (settings.position === 'bottom' || settings.position === 'both') {
    modifiedContent = (
      <>
        {settings.position === 'both' ? modifiedContent : content}
        <div className="mt-6">{socialShareButtons}</div>
      </>
    );
  }
  
  return {
    ...data,
    content: modifiedContent
  };
}

// Social Share Buttons Component
const SocialShareButtons = ({ post, settings }) => {
  const [likes, setLikes] = useState(post.likes || 0);
  const [isLiked, setIsLiked] = useState(false);
  const [shares, setShares] = useState(post.shares || 0);

  const postUrl = `${window.location.origin}/posts/${post.id}`;
  const shareText = `${settings.custom_message} - ${post.title}`;

  const socialPlatforms = {
    facebook: {
      name: 'Facebook',
      icon: Facebook,
      url: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(postUrl)}`,
      color: 'bg-blue-600 hover:bg-blue-700'
    },
    twitter: {
      name: 'Twitter',
      icon: Twitter,
      url: `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(postUrl)}`,
      color: 'bg-sky-500 hover:bg-sky-600'
    },
    linkedin: {
      name: 'LinkedIn',
      icon: Linkedin,
      url: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(postUrl)}`,
      color: 'bg-blue-700 hover:bg-blue-800'
    },
    whatsapp: {
      name: 'WhatsApp',
      icon: MessageCircle,
      url: `https://wa.me/?text=${encodeURIComponent(shareText + ' ' + postUrl)}`,
      color: 'bg-green-500 hover:bg-green-600'
    },
    telegram: {
      name: 'Telegram',
      icon: Send,
      url: `https://t.me/share/url?url=${encodeURIComponent(postUrl)}&text=${encodeURIComponent(shareText)}`,
      color: 'bg-blue-500 hover:bg-blue-600'
    },
    reddit: {
      name: 'Reddit',
      icon: Hash,
      url: `https://reddit.com/submit?url=${encodeURIComponent(postUrl)}&title=${encodeURIComponent(post.title)}`,
      color: 'bg-orange-600 hover:bg-orange-700'
    },
    pinterest: {
      name: 'Pinterest',
      icon: Image,
      url: `https://pinterest.com/pin/create/button/?url=${encodeURIComponent(postUrl)}&description=${encodeURIComponent(shareText)}`,
      color: 'bg-red-600 hover:bg-red-700'
    }
  };

  const handleLike = async () => {
    try {
      // Here you would make an API call to like/unlike the post
      const newLiked = !isLiked;
      const newLikes = newLiked ? likes + 1 : likes - 1;
      
      setIsLiked(newLiked);
      setLikes(newLikes);
      
      // API call would go here
      // await axios.post(`/api/posts/${post.id}/like`, { liked: newLiked });
      
    } catch (error) {
      console.error('Error liking post:', error);
    }
  };

  const handleShare = async (platform) => {
    try {
      // Track share event
      setShares(prev => prev + 1);
      
      // API call to track share
      // await axios.post(`/api/posts/${post.id}/share`, { platform });
      
      // Open share window
      window.open(
        socialPlatforms[platform].url,
        'share',
        'width=600,height=400,scrollbars=yes,resizable=yes'
      );
      
    } catch (error) {
      console.error('Error sharing post:', error);
    }
  };

  const getButtonSize = () => {
    switch (settings.button_size) {
      case 'small': return 'w-8 h-8 text-sm';
      case 'large': return 'w-12 h-12 text-lg';
      default: return 'w-10 h-10 text-base';
    }
  };

  const getButtonStyle = () => {
    switch (settings.button_style) {
      case 'square': return 'rounded-none';
      case 'circular': return 'rounded-full';
      default: return 'rounded-lg';
    }
  };

  const buttonClasses = `${getButtonSize()} ${getButtonStyle()} flex items-center justify-center text-white transition-colors duration-200`;

  return (
    <div className="social-share-plugin border-t border-gray-200 pt-4 mt-4">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        
        {/* Like Button */}
        {settings.show_like_button && (
          <div className="flex items-center space-x-3">
            <button
              onClick={handleLike}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors duration-200 ${
                isLiked 
                  ? 'bg-red-100 text-red-700 hover:bg-red-200' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Heart 
                className={`w-5 h-5 ${isLiked ? 'fill-current' : ''}`} 
              />
              <span className="font-medium">{likes}</span>
              <span className="text-sm">Like{likes !== 1 ? 's' : ''}</span>
            </button>
            
            {settings.show_share_count && (
              <div className="flex items-center space-x-1 text-gray-600">
                <Share2 className="w-4 h-4" />
                <span className="text-sm">{shares} share{shares !== 1 ? 's' : ''}</span>
              </div>
            )}
          </div>
        )}

        {/* Social Share Buttons */}
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-600 mr-2">Share:</span>
          <div className="flex space-x-2">
            {settings.enabled_platforms.map(platform => {
              const Platform = socialPlatforms[platform];
              if (!Platform) return null;
              
              const Icon = Platform.icon;
              
              return (
                <button
                  key={platform}
                  onClick={() => handleShare(platform)}
                  className={`${buttonClasses} ${Platform.color}`}
                  title={`Share on ${Platform.name}`}
                >
                  <Icon className="w-4 h-4" />
                </button>
              );
            })}
          </div>
        </div>
      </div>
      
      {/* Share Count Display */}
      {settings.show_share_count && shares > 0 && (
        <div className="mt-3 text-xs text-gray-500">
          This post has been shared {shares} time{shares !== 1 ? 's' : ''} across social media
        </div>
      )}
    </div>
  );
};

// Social Share Settings Dashboard Component
export const SocialShareSettings = () => {
  const [settings, setSettings] = useState({
    enabled_platforms: ['facebook', 'twitter', 'linkedin', 'whatsapp'],
    button_style: 'rounded',
    button_size: 'medium',
    position: 'bottom',
    show_share_count: true,
    show_like_button: true,
    custom_message: 'Check out this awesome post!'
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleSaveSettings = async () => {
    try {
      setIsLoading(true);
      // API call to save settings
      // await axios.put('/api/plugins/social-media-share-like/settings', { settings });
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      console.log('Settings saved:', settings);
      
    } catch (error) {
      console.error('Error saving settings:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const platforms = [
    { id: 'facebook', name: 'Facebook', icon: Facebook, color: 'text-blue-600' },
    { id: 'twitter', name: 'Twitter', icon: Twitter, color: 'text-sky-500' },
    { id: 'linkedin', name: 'LinkedIn', icon: Linkedin, color: 'text-blue-700' },
    { id: 'whatsapp', name: 'WhatsApp', icon: MessageCircle, color: 'text-green-500' },
    { id: 'telegram', name: 'Telegram', icon: Send, color: 'text-blue-500' },
    { id: 'reddit', name: 'Reddit', icon: Hash, color: 'text-orange-600' },
    { id: 'pinterest', name: 'Pinterest', icon: Image, color: 'text-red-600' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Social Share Settings</h1>
        <button
          onClick={handleSaveSettings}
          disabled={isLoading}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {isLoading ? 'Saving...' : 'Save Settings'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Platform Selection */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Social Platforms</h3>
          <div className="space-y-3">
            {platforms.map(platform => {
              const Icon = platform.icon;
              return (
                <label key={platform.id} className="flex items-center space-x-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.enabled_platforms.includes(platform.id)}
                    onChange={(e) => {
                      const enabled = e.target.checked;
                      setSettings(prev => ({
                        ...prev,
                        enabled_platforms: enabled 
                          ? [...prev.enabled_platforms, platform.id]
                          : prev.enabled_platforms.filter(p => p !== platform.id)
                      }));
                    }}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <Icon className={`w-5 h-5 ${platform.color}`} />
                  <span className="text-sm font-medium">{platform.name}</span>
                </label>
              );
            })}
          </div>
        </div>

        {/* Appearance Settings */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Appearance</h3>
          <div className="space-y-4">
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Button Style
              </label>
              <select
                value={settings.button_style}
                onChange={(e) => setSettings(prev => ({...prev, button_style: e.target.value}))}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
              >
                <option value="rounded">Rounded</option>
                <option value="square">Square</option>
                <option value="circular">Circular</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Button Size
              </label>
              <select
                value={settings.button_size}
                onChange={(e) => setSettings(prev => ({...prev, button_size: e.target.value}))}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
              >
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Position
              </label>
              <select
                value={settings.position}
                onChange={(e) => setSettings(prev => ({...prev, position: e.target.value}))}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
              >
                <option value="top">Top of Post</option>
                <option value="bottom">Bottom of Post</option>
                <option value="both">Both Top & Bottom</option>
                <option value="floating">Floating</option>
              </select>
            </div>
          </div>
        </div>

        {/* Feature Settings */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Features</h3>
          <div className="space-y-4">
            
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.show_like_button}
                onChange={(e) => setSettings(prev => ({...prev, show_like_button: e.target.checked}))}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm font-medium">Enable Like Button</span>
            </label>

            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={settings.show_share_count}
                onChange={(e) => setSettings(prev => ({...prev, show_share_count: e.target.checked}))}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm font-medium">Show Share Count</span>
            </label>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Default Share Message
              </label>
              <input
                type="text"
                value={settings.custom_message}
                onChange={(e) => setSettings(prev => ({...prev, custom_message: e.target.value}))}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                placeholder="Check out this awesome post!"
              />
            </div>
          </div>
        </div>

        {/* Preview */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Preview</h3>
          <div className="border rounded-lg p-4 bg-gray-50">
            <p className="text-sm text-gray-600 mb-4">
              This is how the social share buttons will appear on your posts:
            </p>
            <SocialShareButtons 
              post={{ id: 'preview', title: 'Sample Post', likes: 42, shares: 12 }}
              settings={settings}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
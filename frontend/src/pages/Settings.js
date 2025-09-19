import React, { useState, useEffect } from 'react';
import AdminLayout from '../components/Layout/AdminLayout';
import { Card, CardHeader, CardContent, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Switch } from '../components/ui/switch';
import { useToast } from '../hooks/use-toast';
import { 
  Settings as SettingsIcon,
  Globe,
  Shield,
  Bell,
  Palette,
  Database,
  Mail,
  Save,
  RotateCcw
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Settings = () => {
  const [settings, setSettings] = useState({
    // General Settings
    siteName: 'CMS Pro',
    siteDescription: 'A powerful plugin-based content management system',
    siteUrl: 'https://example.com',
    timezone: 'UTC',
    dateFormat: 'YYYY-MM-DD',
    timeFormat: '24h',
    
    // Security Settings
    twoFactorAuth: false,
    passwordExpiry: false,
    sessionTimeout: 30,
    loginAttempts: 5,
    
    // Email Settings
    emailProvider: 'smtp',
    smtpHost: '',
    smtpPort: 587,
    smtpUsername: '',
    smtpPassword: '',
    
    // Notifications
    emailNotifications: true,
    browserNotifications: false,
    weeklyReports: true,
    
    // Performance
    cacheEnabled: true,
    compressionEnabled: true,
    cdnEnabled: false,
  });

  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      setIsLoading(true);
      // Since we don't have a settings endpoint yet, we'll use local storage
      const savedSettings = localStorage.getItem('cms_settings');
      if (savedSettings) {
        setSettings(prev => ({ ...prev, ...JSON.parse(savedSettings) }));
      }
    } catch (error) {
      console.error('Error loading settings:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      
      // For now, save to localStorage (can be replaced with API call later)
      localStorage.setItem('cms_settings', JSON.stringify(settings));
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      toast({
        title: "Success",
        description: "Settings saved successfully"
      });
    } catch (error) {
      console.error('Error saving settings:', error);
      toast({
        title: "Error",
        description: "Failed to save settings",
        variant: "destructive"
      });
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = () => {
    if (window.confirm('Are you sure you want to reset all settings to defaults?')) {
      setSettings({
        siteName: 'CMS Pro',
        siteDescription: 'A powerful plugin-based content management system',
        siteUrl: 'https://example.com',
        timezone: 'UTC',
        dateFormat: 'YYYY-MM-DD',
        timeFormat: '24h',
        twoFactorAuth: false,
        passwordExpiry: false,
        sessionTimeout: 30,
        loginAttempts: 5,
        emailProvider: 'smtp',
        smtpHost: '',
        smtpPort: 587,
        smtpUsername: '',
        smtpPassword: '',
        emailNotifications: true,
        browserNotifications: false,
        weeklyReports: true,
        cacheEnabled: true,
        compressionEnabled: true,
        cdnEnabled: false,
      });
      
      localStorage.removeItem('cms_settings');
      
      toast({
        title: "Success",
        description: "Settings reset to defaults"
      });
    }
  };

  const settingSections = [
    {
      id: 'general',
      title: 'General Settings',
      icon: Globe,
      description: 'Basic site configuration'
    },
    {
      id: 'security',
      title: 'Security',
      icon: Shield,
      description: 'Security and authentication settings'
    },
    {
      id: 'email',
      title: 'Email Configuration',
      icon: Mail,
      description: 'SMTP and email settings'
    },
    {
      id: 'notifications',
      title: 'Notifications',
      icon: Bell,
      description: 'Notification preferences'
    },
    {
      id: 'performance',
      title: 'Performance',
      icon: Database,
      description: 'Caching and optimization settings'
    }
  ];

  const [activeSection, setActiveSection] = useState('general');

  const renderGeneralSettings = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <Label htmlFor="siteName">Site Name</Label>
          <Input
            id="siteName"
            value={settings.siteName}
            onChange={(e) => handleSettingChange('siteName', e.target.value)}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="siteUrl">Site URL</Label>
          <Input
            id="siteUrl"
            value={settings.siteUrl}
            onChange={(e) => handleSettingChange('siteUrl', e.target.value)}
          />
        </div>
      </div>
      
      <div className="space-y-2">
        <Label htmlFor="siteDescription">Site Description</Label>
        <Textarea
          id="siteDescription"
          value={settings.siteDescription}
          onChange={(e) => handleSettingChange('siteDescription', e.target.value)}
          rows={3}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="space-y-2">
          <Label htmlFor="timezone">Timezone</Label>
          <select
            id="timezone"
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={settings.timezone}
            onChange={(e) => handleSettingChange('timezone', e.target.value)}
          >
            <option value="UTC">UTC</option>
            <option value="America/New_York">Eastern Time</option>
            <option value="America/Los_Angeles">Pacific Time</option>
            <option value="Europe/London">London</option>
          </select>
        </div>
        <div className="space-y-2">
          <Label htmlFor="dateFormat">Date Format</Label>
          <select
            id="dateFormat"
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={settings.dateFormat}
            onChange={(e) => handleSettingChange('dateFormat', e.target.value)}
          >
            <option value="YYYY-MM-DD">YYYY-MM-DD</option>
            <option value="MM/DD/YYYY">MM/DD/YYYY</option>
            <option value="DD/MM/YYYY">DD/MM/YYYY</option>
          </select>
        </div>
        <div className="space-y-2">
          <Label htmlFor="timeFormat">Time Format</Label>
          <select
            id="timeFormat"
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={settings.timeFormat}
            onChange={(e) => handleSettingChange('timeFormat', e.target.value)}
          >
            <option value="24h">24 Hour</option>
            <option value="12h">12 Hour</option>
          </select>
        </div>
      </div>
    </div>
  );

  const renderSecuritySettings = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
        <div>
          <h4 className="font-medium text-gray-900">Two-Factor Authentication</h4>
          <p className="text-sm text-gray-500">Add an extra layer of security to your account</p>
        </div>
        <Switch
          checked={settings.twoFactorAuth}
          onCheckedChange={(checked) => handleSettingChange('twoFactorAuth', checked)}
        />
      </div>

      <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
        <div>
          <h4 className="font-medium text-gray-900">Password Expiry</h4>
          <p className="text-sm text-gray-500">Require password changes every 90 days</p>
        </div>
        <Switch
          checked={settings.passwordExpiry}
          onCheckedChange={(checked) => handleSettingChange('passwordExpiry', checked)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <Label htmlFor="sessionTimeout">Session Timeout (minutes)</Label>
          <Input
            id="sessionTimeout"
            type="number"
            value={settings.sessionTimeout}
            onChange={(e) => handleSettingChange('sessionTimeout', parseInt(e.target.value))}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="loginAttempts">Max Login Attempts</Label>
          <Input
            id="loginAttempts"
            type="number"
            value={settings.loginAttempts}
            onChange={(e) => handleSettingChange('loginAttempts', parseInt(e.target.value))}
          />
        </div>
      </div>
    </div>
  );

  const renderEmailSettings = () => (
    <div className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="emailProvider">Email Provider</Label>
        <select
          id="emailProvider"
          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          value={settings.emailProvider}
          onChange={(e) => handleSettingChange('emailProvider', e.target.value)}
        >
          <option value="smtp">SMTP</option>
          <option value="sendgrid">SendGrid</option>
          <option value="mailgun">Mailgun</option>
        </select>
      </div>

      {settings.emailProvider === 'smtp' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <Label htmlFor="smtpHost">SMTP Host</Label>
            <Input
              id="smtpHost"
              value={settings.smtpHost}
              onChange={(e) => handleSettingChange('smtpHost', e.target.value)}
              placeholder="smtp.gmail.com"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="smtpPort">SMTP Port</Label>
            <Input
              id="smtpPort"
              type="number"
              value={settings.smtpPort}
              onChange={(e) => handleSettingChange('smtpPort', parseInt(e.target.value))}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="smtpUsername">Username</Label>
            <Input
              id="smtpUsername"
              value={settings.smtpUsername}
              onChange={(e) => handleSettingChange('smtpUsername', e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="smtpPassword">Password</Label>
            <Input
              id="smtpPassword"
              type="password"
              value={settings.smtpPassword}
              onChange={(e) => handleSettingChange('smtpPassword', e.target.value)}
            />
          </div>
        </div>
      )}
    </div>
  );

  const renderNotificationSettings = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
        <div>
          <h4 className="font-medium text-gray-900">Email Notifications</h4>
          <p className="text-sm text-gray-500">Receive notifications via email</p>
        </div>
        <Switch
          checked={settings.emailNotifications}
          onCheckedChange={(checked) => handleSettingChange('emailNotifications', checked)}
        />
      </div>

      <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
        <div>
          <h4 className="font-medium text-gray-900">Browser Notifications</h4>
          <p className="text-sm text-gray-500">Show desktop notifications</p>
        </div>
        <Switch
          checked={settings.browserNotifications}
          onCheckedChange={(checked) => handleSettingChange('browserNotifications', checked)}
        />
      </div>

      <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
        <div>
          <h4 className="font-medium text-gray-900">Weekly Reports</h4>
          <p className="text-sm text-gray-500">Receive weekly activity summaries</p>
        </div>
        <Switch
          checked={settings.weeklyReports}
          onCheckedChange={(checked) => handleSettingChange('weeklyReports', checked)}
        />
      </div>
    </div>
  );

  const renderPerformanceSettings = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
        <div>
          <h4 className="font-medium text-gray-900">Cache Enabled</h4>
          <p className="text-sm text-gray-500">Enable caching to improve performance</p>
        </div>
        <Switch
          checked={settings.cacheEnabled}
          onCheckedChange={(checked) => handleSettingChange('cacheEnabled', checked)}
        />
      </div>

      <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
        <div>
          <h4 className="font-medium text-gray-900">Compression</h4>
          <p className="text-sm text-gray-500">Enable GZIP compression</p>
        </div>
        <Switch
          checked={settings.compressionEnabled}
          onCheckedChange={(checked) => handleSettingChange('compressionEnabled', checked)}
        />
      </div>

      <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
        <div>
          <h4 className="font-medium text-gray-900">CDN</h4>
          <p className="text-sm text-gray-500">Use Content Delivery Network</p>
        </div>
        <Switch
          checked={settings.cdnEnabled}
          onCheckedChange={(checked) => handleSettingChange('cdnEnabled', checked)}
        />
      </div>
    </div>
  );

  const renderSettingContent = () => {
    switch (activeSection) {
      case 'general': return renderGeneralSettings();
      case 'security': return renderSecuritySettings();
      case 'email': return renderEmailSettings();
      case 'notifications': return renderNotificationSettings();
      case 'performance': return renderPerformanceSettings();
      default: return renderGeneralSettings();
    }
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
            <p className="text-gray-600">Configure your CMS preferences and options</p>
          </div>
          <div className="flex space-x-3">
            <Button variant="outline" onClick={handleReset} disabled={isSaving}>
              <RotateCcw className="w-4 h-4 mr-2" />
              Reset
            </Button>
            <Button onClick={handleSave} disabled={isSaving}>
              <Save className="w-4 h-4 mr-2" />
              {isSaving ? 'Saving...' : 'Save Changes'}
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Settings Navigation */}
          <Card className="lg:col-span-1">
            <CardHeader>
              <CardTitle className="text-lg">Settings</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <nav className="space-y-1">
                {settingSections.map((section) => {
                  const Icon = section.icon;
                  return (
                    <button
                      key={section.id}
                      onClick={() => setActiveSection(section.id)}
                      className={`w-full text-left px-4 py-3 flex items-center space-x-3 hover:bg-gray-50 transition-colors ${
                        activeSection === section.id
                          ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-600'
                          : 'text-gray-700'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <div>
                        <p className="font-medium">{section.title}</p>
                        <p className="text-xs text-gray-500">{section.description}</p>
                      </div>
                    </button>
                  );
                })}
              </nav>
            </CardContent>
          </Card>

          {/* Settings Content */}
          <div className="lg:col-span-3">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  {settingSections.find(s => s.id === activeSection)?.icon && (
                    React.createElement(settingSections.find(s => s.id === activeSection).icon, {
                      className: "w-5 h-5 mr-2"
                    })
                  )}
                  {settingSections.find(s => s.id === activeSection)?.title}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {renderSettingContent()}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

export default Settings;
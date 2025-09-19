import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { usePlugins } from '../contexts/PluginContext';
import { useNavigate } from 'react-router-dom';
import AdminLayout from '../components/Layout/AdminLayout';
import { Card, CardHeader, CardContent, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { 
  FileText, 
  File, 
  Users, 
  Puzzle,
  TrendingUp,
  Activity,
  Eye,
  MessageSquare
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const { user } = useAuth();
  const { plugins, activePlugins, executeHook } = usePlugins();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [recentActivity, setRecentActivity] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      const [statsResponse, activityResponse] = await Promise.all([
        axios.get(`${API}/dashboard/stats`),
        axios.get(`${API}/dashboard/activity?limit=5`)
      ]);
      
      setStats(statsResponse.data);
      setRecentActivity(activityResponse.data.activity_feed || []);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      // Fallback to basic stats
      setStats({
        total_posts: 0,
        total_pages: 0,
        total_users: 0,
        active_plugins: activePlugins.length
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <AdminLayout>
        <div className="space-y-6">
          <div className="animate-pulse space-y-6">
            <div className="h-32 bg-gray-200 rounded-lg"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
              ))}
            </div>
          </div>
        </div>
      </AdminLayout>
    );
  }

  const statsCards = [
    {
      title: 'Total Posts',
      value: stats?.total_posts || 0,
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      change: '+12%'
    },
    {
      title: 'Pages',
      value: stats?.total_pages || 0,
      icon: File,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      change: '+5%'
    },
    {
      title: 'Users',
      value: stats?.total_users || 0,
      icon: Users,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      change: '+8%'
    },
    {
      title: 'Active Plugins',
      value: stats?.active_plugins || 0,
      icon: Puzzle,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
      change: `${activePlugins.length}/${plugins.length}`
    }
  ];

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Welcome Message */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg p-6 text-white">
          <h1 className="text-2xl font-bold mb-2">
            Welcome back, {user?.name}! 👋
          </h1>
          <p className="text-blue-100">
            Here's what's happening with your CMS today.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {statsCards.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <Card key={index} className="hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">
                        {stat.title}
                      </p>
                      <p className="text-3xl font-bold text-gray-900">
                        {stat.value}
                      </p>
                    </div>
                    <div className={`${stat.bgColor} p-3 rounded-lg`}>
                      <Icon className={`w-6 h-6 ${stat.color}`} />
                    </div>
                  </div>
                  <div className="mt-4 flex items-center">
                    <Badge variant="secondary" className="text-xs">
                      {stat.change}
                    </Badge>
                    <span className="text-xs text-gray-500 ml-2">vs last month</span>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Activity className="w-5 h-5 mr-2" />
                Recent Activity
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentActivity.length > 0 ? (
                  recentActivity.map((activity, index) => {
                    const iconName = activity.icon || 'Activity';
                    const IconComponent = {
                      FileText,
                      File,
                      Users,
                      Puzzle,
                      Activity
                    }[iconName] || Activity;
                    
                    return (
                      <div key={index} className="flex items-start space-x-3">
                        <div className="bg-gray-100 p-2 rounded-lg">
                          <IconComponent className="w-4 h-4 text-gray-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm text-gray-900">{activity.title || activity.message}</p>
                          <p className="text-xs text-gray-500">
                            {activity.time || new Date(activity.timestamp).toRelativeTimeString?.() || 'Recently'}
                          </p>
                        </div>
                      </div>
                    );
                  })
                ) : (
                  <p className="text-gray-500 text-sm">No recent activity</p>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4">
                <button 
                  onClick={() => navigate('/admin/posts')}
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left"
                >
                  <FileText className="w-8 h-8 text-blue-600 mb-2" />
                  <h3 className="font-medium text-gray-900">New Post</h3>
                  <p className="text-sm text-gray-500">Create a new blog post</p>
                </button>
                <button 
                  onClick={() => navigate('/admin/pages')}
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left"
                >
                  <File className="w-8 h-8 text-green-600 mb-2" />
                  <h3 className="font-medium text-gray-900">New Page</h3>
                  <p className="text-sm text-gray-500">Add a new page</p>
                </button>
                <button 
                  onClick={() => navigate('/admin/plugins')}
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left"
                >
                  <Puzzle className="w-8 h-8 text-purple-600 mb-2" />
                  <h3 className="font-medium text-gray-900">Browse Plugins</h3>
                  <p className="text-sm text-gray-500">Extend functionality</p>
                </button>
                <button 
                  onClick={() => navigate('/admin/users')}
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left"
                >
                  <Users className="w-8 h-8 text-orange-600 mb-2" />
                  <h3 className="font-medium text-gray-900">Manage Users</h3>
                  <p className="text-sm text-gray-500">User roles & permissions</p>
                </button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Plugin Showcase */}
        {activePlugins.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Puzzle className="w-5 h-5 mr-2" />
                Active Plugins
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {activePlugins.slice(0, 3).map(pluginId => {
                  const plugin = plugins.find(p => p.id === pluginId);
                  if (!plugin) return null;
                  
                  return (
                    <div key={pluginId} className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg">
                      <img 
                        src={plugin.icon} 
                        alt={plugin.name}
                        className="w-10 h-10 rounded"
                        onError={(e) => {
                          e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0yMCAzMEMxNS4wMyAzMCAxMS4wNTcgMjUuNTIgMTEuMDU3IDIwQzExLjA1NyAxNC40OCAxNS4wMyAxMCAyMCAxMEMyNC45NyAxMCAyOC45NDMgMTQuNDggMjguOTQzIDIwQzI4Ljk0MyAyNS41MiAyNC45NyAzMCAyMCAzMFoiIGZpbGw9IiM5Q0EzQUYiLz4KPC9zdmc+';
                        }}
                      />
                      <div>
                        <h4 className="font-medium text-gray-900">{plugin.name}</h4>
                        <p className="text-sm text-gray-500">v{plugin.version}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </AdminLayout>
  );
};

export default Dashboard;
import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { usePlugins } from '../contexts/PluginContext';
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
import { mockPosts, mockPages, mockUsers } from '../data/mock';

const Dashboard = () => {
  const { user } = useAuth();
  const { plugins, activePlugins, executeHook } = usePlugins();

  const stats = [
    {
      title: 'Total Posts',
      value: mockPosts.length,
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      change: '+12%'
    },
    {
      title: 'Pages',
      value: mockPages.length,
      icon: File,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      change: '+5%'
    },
    {
      title: 'Users',
      value: mockUsers.length,
      icon: Users,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      change: '+8%'
    },
    {
      title: 'Active Plugins',
      value: activePlugins.length,
      icon: Puzzle,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
      change: `${activePlugins.length}/${plugins.length}`
    }
  ];

  const recentActivity = [
    {
      type: 'post',
      message: 'New post "Building with Plugins" was published',
      time: '2 hours ago',
      icon: FileText
    },
    {
      type: 'plugin',
      message: 'Contact Form 7 plugin was activated',
      time: '4 hours ago',
      icon: Puzzle
    },
    {
      type: 'user',
      message: 'New user registration: Author User',
      time: '1 day ago',
      icon: Users
    }
  ];

  // Allow plugins to modify dashboard data
  const dashboardData = executeHook('dashboard_stats', { stats, recentActivity });

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
          {(dashboardData.stats || stats).map((stat, index) => {
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
                {(dashboardData.recentActivity || recentActivity).map((activity, index) => {
                  const Icon = activity.icon;
                  return (
                    <div key={index} className="flex items-start space-x-3">
                      <div className="bg-gray-100 p-2 rounded-lg">
                        <Icon className="w-4 h-4 text-gray-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-gray-900">{activity.message}</p>
                        <p className="text-xs text-gray-500">{activity.time}</p>
                      </div>
                    </div>
                  );
                })}
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
                <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left">
                  <FileText className="w-8 h-8 text-blue-600 mb-2" />
                  <h3 className="font-medium text-gray-900">New Post</h3>
                  <p className="text-sm text-gray-500">Create a new blog post</p>
                </button>
                <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left">
                  <File className="w-8 h-8 text-green-600 mb-2" />
                  <h3 className="font-medium text-gray-900">New Page</h3>
                  <p className="text-sm text-gray-500">Add a new page</p>
                </button>
                <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left">
                  <Puzzle className="w-8 h-8 text-purple-600 mb-2" />
                  <h3 className="font-medium text-gray-900">Browse Plugins</h3>
                  <p className="text-sm text-gray-500">Extend functionality</p>
                </button>
                <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left">
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
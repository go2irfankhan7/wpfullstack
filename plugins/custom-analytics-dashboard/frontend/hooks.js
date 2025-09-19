// Frontend hooks for Custom Analytics Plugin
import React from 'react';
import { BarChart3, TrendingUp, Users, Activity } from 'lucide-react';

// Hook to add Analytics menu item to admin sidebar
export function admin_menu(menuItems) {
  return [
    ...menuItems,
    {
      title: 'Analytics',
      path: '/admin/analytics',
      icon: BarChart3,
      roles: ['admin', 'editor']
    }
  ];
}

// Hook to add custom widgets to dashboard
export function dashboard_stats(data) {
  const customStats = [
    ...data.stats,
    {
      title: 'Page Views',
      value: '12,543',
      icon: TrendingUp,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      change: '+23%'
    },
    {
      title: 'Unique Visitors', 
      value: '3,247',
      icon: Users,
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-50',
      change: '+15%'
    }
  ];

  const customActivity = [
    {
      type: 'analytics',
      title: 'Traffic spike detected',
      description: 'Page views increased by 45% today',
      timestamp: new Date().toISOString(),
      icon: 'TrendingUp'
    },
    ...data.recent_activity
  ];

  return {
    ...data,
    stats: customStats,
    recent_activity: customActivity
  };
}

// Custom Analytics Dashboard Component
export const AnalyticsDashboard = () => {
  const analyticsData = {
    pageViews: 12543,
    uniqueVisitors: 3247,
    bounceRate: '32%',
    avgSessionDuration: '2m 45s'
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          Export Report
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Page Views</p>
              <p className="text-3xl font-bold text-gray-900">{analyticsData.pageViews.toLocaleString()}</p>
            </div>
            <div className="bg-purple-50 p-3 rounded-lg">
              <TrendingUp className="w-6 h-6 text-purple-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Unique Visitors</p>
              <p className="text-3xl font-bold text-gray-900">{analyticsData.uniqueVisitors.toLocaleString()}</p>
            </div>
            <div className="bg-indigo-50 p-3 rounded-lg">
              <Users className="w-6 h-6 text-indigo-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Bounce Rate</p>
              <p className="text-3xl font-bold text-gray-900">{analyticsData.bounceRate}</p>
            </div>
            <div className="bg-green-50 p-3 rounded-lg">
              <Activity className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Avg. Session</p>
              <p className="text-3xl font-bold text-gray-900">{analyticsData.avgSessionDuration}</p>
            </div>
            <div className="bg-yellow-50 p-3 rounded-lg">
              <BarChart3 className="w-6 h-6 text-yellow-600" />
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-4">Traffic Overview</h3>
        <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
          <p className="text-gray-500">Analytics chart would go here</p>
        </div>
      </div>
    </div>
  );
};
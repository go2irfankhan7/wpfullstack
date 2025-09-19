import React, { useState } from 'react';
import AdminLayout from '../components/Layout/AdminLayout';
import { usePlugins } from '../contexts/PluginContext';
import { Card, CardHeader, CardContent, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../components/ui/dialog';
import { useToast } from '../hooks/use-toast';
import { 
  Puzzle,
  Download,
  Settings,
  Trash2,
  Search,
  Filter,
  Star,
  Package,
  Zap,
  Shield,
  Eye,
  ExternalLink,
  Upload,
  X,
  CheckCircle,
  AlertCircle
} from 'lucide-react';

const Plugins = () => {
  const { plugins, activePlugins, activatePlugin, deactivatePlugin, isPluginActive, installPlugin } = usePlugins();
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [showInstalled, setShowInstalled] = useState(false);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [uploadFile, setUploadFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const { toast } = useToast();

  const filteredPlugins = plugins.filter(plugin => {
    const matchesSearch = plugin.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         plugin.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = categoryFilter === 'all' || plugin.category === categoryFilter;
    const matchesInstalled = !showInstalled || isPluginActive(plugin.id);
    return matchesSearch && matchesCategory && matchesInstalled;
  });

  const categories = [...new Set(plugins.map(p => p.category))];

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'Forms': return Package;
      case 'SEO': return Zap;
      case 'E-commerce': return Shield;
      case 'Utility': return Settings;
      default: return Puzzle;
    }
  };

  const handlePluginToggle = (pluginId) => {
    if (isPluginActive(pluginId)) {
      deactivatePlugin(pluginId);
    } else {
      activatePlugin(pluginId);
    }
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Plugins</h1>
            <p className="text-gray-600">Extend your CMS with powerful plugins</p>
          </div>
          <div className="flex space-x-3">
            <Button variant="outline">
              <Package className="w-4 h-4 mr-2" />
              Upload Plugin
            </Button>
            <Button>
              <Download className="w-4 h-4 mr-2" />
              Browse Store
            </Button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Plugins</p>
                  <p className="text-3xl font-bold text-gray-900">{plugins.length}</p>
                </div>
                <div className="bg-blue-50 p-3 rounded-lg">
                  <Puzzle className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Active Plugins</p>
                  <p className="text-3xl font-bold text-green-600">{activePlugins.length}</p>
                </div>
                <div className="bg-green-50 p-3 rounded-lg">
                  <Zap className="w-6 h-6 text-green-600" />
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Categories</p>
                  <p className="text-3xl font-bold text-purple-600">{categories.length}</p>
                </div>
                <div className="bg-purple-50 p-3 rounded-lg">
                  <Package className="w-6 h-6 text-purple-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card>
          <CardContent className="p-6">
            <div className="flex flex-col sm:flex-row gap-4">
              {/* Search */}
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <input
                    type="text"
                    placeholder="Search plugins..."
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>

              {/* Category Filter */}
              <div className="flex items-center space-x-2">
                <Filter className="w-4 h-4 text-gray-400" />
                <select
                  className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={categoryFilter}
                  onChange={(e) => setCategoryFilter(e.target.value)}
                >
                  <option value="all">All Categories</option>
                  {categories.map(category => (
                    <option key={category} value={category}>{category}</option>
                  ))}
                </select>
              </div>

              {/* Show Installed */}
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={showInstalled}
                  onChange={(e) => setShowInstalled(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">Show installed only</span>
              </label>
            </div>
          </CardContent>
        </Card>

        {/* Plugins Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredPlugins.map(plugin => {
            const CategoryIcon = getCategoryIcon(plugin.category);
            const isActive = isPluginActive(plugin.id);
            
            return (
              <Card key={plugin.id} className="hover:shadow-md transition-shadow">
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      <img
                        src={plugin.icon}
                        alt={plugin.name}
                        className="w-12 h-12 rounded-lg"
                      />
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{plugin.name}</h3>
                        <div className="flex items-center space-x-2">
                          <Badge variant="secondary" className="text-xs">
                            v{plugin.version}
                          </Badge>
                          <Badge variant="outline" className="text-xs">
                            {plugin.category}
                          </Badge>
                          {plugin.price === 'Free' ? (
                            <Badge className="bg-green-100 text-green-800 text-xs">Free</Badge>
                          ) : (
                            <Badge className="bg-blue-100 text-blue-800 text-xs">{plugin.price}</Badge>
                          )}
                        </div>
                      </div>
                    </div>
                    {isActive && (
                      <Badge className="bg-green-100 text-green-800">
                        <Zap className="w-3 h-3 mr-1" />
                        Active
                      </Badge>
                    )}
                  </div>
                </CardHeader>

                <CardContent>
                  <p className="text-gray-600 mb-4">{plugin.description}</p>

                  {/* Features */}
                  <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Features:</h4>
                    <div className="grid grid-cols-2 gap-1 text-sm text-gray-600">
                      {plugin.features.slice(0, 4).map((feature, index) => (
                        <div key={index} className="flex items-center space-x-1">
                          <Star className="w-3 h-3 text-yellow-400" />
                          <span>{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="text-sm text-gray-500 mb-4">
                    By {plugin.author}
                  </div>

                  {/* Actions */}
                  <div className="flex space-x-2">
                    {isActive ? (
                      <>
                        <Button 
                          variant="outline" 
                          className="flex-1 text-red-600 hover:bg-red-50"
                          onClick={() => handlePluginToggle(plugin.id)}
                        >
                          Deactivate
                        </Button>
                        <Button variant="outline" size="sm">
                          <Settings className="w-4 h-4" />
                        </Button>
                      </>
                    ) : (
                      <Button 
                        className="flex-1"
                        onClick={() => handlePluginToggle(plugin.id)}
                      >
                        <Zap className="w-4 h-4 mr-2" />
                        Activate
                      </Button>
                    )}
                    <Button variant="outline" size="sm">
                      <Eye className="w-4 h-4" />
                    </Button>
                    <Button variant="outline" size="sm">
                      <ExternalLink className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {filteredPlugins.length === 0 && (
          <Card>
            <CardContent className="p-12 text-center">
              <div className="text-gray-400 mb-4">
                <Puzzle className="w-12 h-12 mx-auto" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No plugins found</h3>
              <p className="text-gray-500 mb-4">
                {searchTerm || categoryFilter !== 'all' || showInstalled
                  ? 'Try adjusting your search or filter criteria'
                  : 'Browse the plugin store to find extensions for your CMS'
                }
              </p>
              <Button>
                <Download className="w-4 h-4 mr-2" />
                Browse Plugin Store
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </AdminLayout>
  );
};

export default Plugins;
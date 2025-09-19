import React, { useState } from 'react';
import AdminLayout from '../components/Layout/AdminLayout';
import { Card, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { 
  Plus, 
  Edit, 
  Trash2, 
  Eye,
  Search,
  File,
  Globe,
  Layout,
  MoreHorizontal
} from 'lucide-react';
import { mockPages } from '../data/mock';

const Pages = () => {
  const [pages, setPages] = useState(mockPages);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredPages = pages.filter(page => {
    return page.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
           page.content.toLowerCase().includes(searchTerm.toLowerCase());
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'published': return 'bg-green-100 text-green-800';
      case 'draft': return 'bg-yellow-100 text-yellow-800';
      case 'private': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleDeletePage = (pageId) => {
    setPages(prev => prev.filter(p => p.id !== pageId));
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Pages</h1>
            <p className="text-gray-600">Manage static pages and content</p>
          </div>
          <Button className="flex items-center space-x-2">
            <Plus className="w-4 h-4" />
            <span>New Page</span>
          </Button>
        </div>

        {/* Search */}
        <Card>
          <CardContent className="p-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search pages..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </CardContent>
        </Card>

        {/* Pages Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPages.map(page => (
            <Card key={page.id} className="hover:shadow-md transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <File className="w-5 h-5 text-blue-600" />
                    </div>
                    <Badge className={getStatusColor(page.status)}>
                      {page.status}
                    </Badge>
                  </div>
                  <Button variant="ghost" size="sm">
                    <MoreHorizontal className="w-4 h-4" />
                  </Button>
                </div>

                <h3 className="text-lg font-semibold text-gray-900 mb-2 hover:text-blue-600 cursor-pointer">
                  {page.title}
                </h3>

                <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                  {page.content.substring(0, 120)}...
                </p>

                <div className="space-y-2 mb-4 text-sm text-gray-500">
                  <div className="flex items-center space-x-2">
                    <Globe className="w-4 h-4" />
                    <span>/{page.slug}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Layout className="w-4 h-4" />
                    <span>Template: {page.template}</span>
                  </div>
                  <div>
                    <span>By {page.author}</span>
                  </div>
                  <div>
                    <span>Modified: {new Date(page.updatedAt).toLocaleDateString()}</span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex space-x-2 pt-4 border-t border-gray-200">
                  <Button variant="outline" size="sm" className="flex-1">
                    <Edit className="w-4 h-4 mr-1" />
                    Edit
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1">
                    <Eye className="w-4 h-4 mr-1" />
                    View
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm"
                    className="text-red-600 hover:bg-red-50"
                    onClick={() => handleDeletePage(page.id)}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Add New Page Card */}
        <Card className="border-dashed border-2 border-gray-300 hover:border-blue-400 transition-colors cursor-pointer">
          <CardContent className="p-12 text-center">
            <div className="text-gray-400 mb-4">
              <Plus className="w-12 h-12 mx-auto" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Create New Page</h3>
            <p className="text-gray-500 mb-4">
              Add a new static page to your website
            </p>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              New Page
            </Button>
          </CardContent>
        </Card>

        {filteredPages.length === 0 && searchTerm && (
          <Card>
            <CardContent className="p-12 text-center">
              <div className="text-gray-400 mb-4">
                <File className="w-12 h-12 mx-auto" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No pages found</h3>
              <p className="text-gray-500">
                No pages match your search criteria
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </AdminLayout>
  );
};

export default Pages;
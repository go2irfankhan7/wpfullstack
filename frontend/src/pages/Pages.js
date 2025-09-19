import React, { useState, useEffect } from 'react';
import AdminLayout from '../components/Layout/AdminLayout';
import { Card, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { useToast } from '../hooks/use-toast';
import { 
  Plus, 
  Edit, 
  Trash2, 
  Eye,
  Search,
  File,
  Globe,
  Layout,
  MoreHorizontal,
  Save,
  X
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Pages = () => {
  const [pages, setPages] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedPage, setSelectedPage] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    slug: '',
    status: 'draft',
    template: 'default'
  });
  const { toast } = useToast();

  useEffect(() => {
    loadPages();
  }, []);

  const loadPages = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get(`${API}/pages`);
      setPages(response.data);
    } catch (error) {
      console.error('Error loading pages:', error);
      toast({
        title: "Error",
        description: "Failed to load pages",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

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

  const handleCreatePage = () => {
    setFormData({
      title: '',
      content: '',
      slug: '',
      status: 'draft',
      template: 'default'
    });
    setIsCreateModalOpen(true);
  };

  const handleEditPage = (page) => {
    setSelectedPage(page);
    setFormData({
      title: page.title,
      content: page.content,
      slug: page.slug,
      status: page.status,
      template: page.template
    });
    setIsEditModalOpen(true);
  };

  const handleSavePage = async () => {
    try {
      if (!formData.title.trim() || !formData.content.trim()) {
        toast({
          title: "Error",
          description: "Please fill in all required fields",
          variant: "destructive"
        });
        return;
      }

      if (selectedPage) {
        // Update existing page
        await axios.put(`${API}/pages/${selectedPage.id}`, formData);
        toast({
          title: "Success",
          description: "Page updated successfully"
        });
        setIsEditModalOpen(false);
      } else {
        // Create new page
        await axios.post(`${API}/pages`, formData);
        toast({
          title: "Success",
          description: "Page created successfully"
        });
        setIsCreateModalOpen(false);
      }
      
      loadPages(); // Reload pages
      setSelectedPage(null);
    } catch (error) {
      console.error('Error saving page:', error);
      toast({
        title: "Error",
        description: error.response?.data?.detail || "Failed to save page",
        variant: "destructive"
      });
    }
  };

  const handleDeletePage = async (pageId) => {
    if (window.confirm('Are you sure you want to delete this page?')) {
      try {
        await axios.delete(`${API}/pages/${pageId}`);
        toast({
          title: "Success",
          description: "Page deleted successfully"
        });
        loadPages();
      } catch (error) {
        console.error('Error deleting page:', error);
        toast({
          title: "Error",
          description: "Failed to delete page",
          variant: "destructive"
        });
      }
    }
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Auto-generate slug from title
    if (name === 'title' && !selectedPage) {
      const slug = value
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim('-');
      setFormData(prev => ({
        ...prev,
        slug: slug
      }));
    }
  };

  if (isLoading) {
    return (
      <AdminLayout>
        <div className="space-y-6">
          <div className="animate-pulse space-y-6">
            <div className="h-8 bg-gray-200 rounded w-1/4"></div>
            <div className="h-12 bg-gray-200 rounded"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="h-48 bg-gray-200 rounded-lg"></div>
              ))}
            </div>
          </div>
        </div>
      </AdminLayout>
    );
  }

  const PageModal = ({ isOpen, onClose, title, isEdit = false }) => (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="title">Title *</Label>
              <Input
                id="title"
                name="title"
                value={formData.title}
                onChange={handleFormChange}
                placeholder="Page title"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="slug">Slug</Label>
              <Input
                id="slug"
                name="slug"
                value={formData.slug}
                onChange={handleFormChange}
                placeholder="page-url-slug"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="content">Content *</Label>
            <Textarea
              id="content"
              name="content"
              value={formData.content}
              onChange={handleFormChange}
              placeholder="Page content..."
              className="min-h-[200px]"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="status">Status</Label>
              <select
                id="status"
                name="status"
                value={formData.status}
                onChange={handleFormChange}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="draft">Draft</option>
                <option value="published">Published</option>
                <option value="private">Private</option>
              </select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="template">Template</Label>
              <select
                id="template"
                name="template"
                value={formData.template}
                onChange={handleFormChange}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="default">Default</option>
                <option value="contact">Contact</option>
                <option value="about">About</option>
                <option value="landing">Landing</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <Button variant="outline" onClick={() => onClose(false)}>
              <X className="w-4 h-4 mr-2" />
              Cancel
            </Button>
            <Button onClick={handleSavePage}>
              <Save className="w-4 h-4 mr-2" />
              {isEdit ? 'Update Page' : 'Create Page'}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Pages</h1>
            <p className="text-gray-600">Manage static pages and content</p>
          </div>
          <Button onClick={handleCreatePage} className="flex items-center space-x-2">
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
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="flex-1"
                    onClick={() => handleEditPage(page)}
                  >
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

          {/* Add New Page Card */}
          <Card 
            className="border-dashed border-2 border-gray-300 hover:border-blue-400 transition-colors cursor-pointer"
            onClick={handleCreatePage}
          >
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
        </div>

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

        {/* Create Page Modal */}
        <PageModal 
          isOpen={isCreateModalOpen} 
          onClose={setIsCreateModalOpen}
          title="Create New Page"
        />

        {/* Edit Page Modal */}
        <PageModal 
          isOpen={isEditModalOpen} 
          onClose={setIsEditModalOpen}
          title="Edit Page"
          isEdit={true}
        />
      </div>
    </AdminLayout>
  );
};

export default Pages;
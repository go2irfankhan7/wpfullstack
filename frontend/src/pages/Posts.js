import React, { useState, useEffect } from 'react';
import AdminLayout from '../components/Layout/AdminLayout';
import { Card, CardHeader, CardContent, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../components/ui/dialog';
import { useToast } from '../hooks/use-toast';
import { 
  Plus, 
  Edit, 
  Trash2, 
  Eye,
  Search,
  Filter,
  MoreHorizontal,
  Save,
  X,
  FileText
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Posts = () => {
  const [posts, setPosts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [viewPost, setViewPost] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    excerpt: '',
    status: 'draft',
    category: '',
    tags: '',
    featured_image: ''
  });
  const { toast } = useToast();

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get(`${API}/posts`);
      setPosts(response.data);
    } catch (error) {
      console.error('Error loading posts:', error);
      toast({
        title: "Error",
        description: "Failed to load posts",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const filteredPosts = posts.filter(post => {
    const matchesSearch = post.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         post.content?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || post.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'published': return 'bg-green-100 text-green-800';
      case 'draft': return 'bg-yellow-100 text-yellow-800';
      case 'private': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleCreatePost = () => {
    setFormData({
      title: '',
      content: '',
      excerpt: '',
      status: 'draft',
      category: '',
      tags: '',
      featured_image: ''
    });
    setIsCreateModalOpen(true);
  };

  const handleEditPost = (post) => {
    setSelectedPost(post);
    setFormData({
      title: post.title || '',
      content: post.content || '',
      excerpt: post.excerpt || '',
      status: post.status || 'draft',
      category: post.category || '',
      tags: Array.isArray(post.tags) ? post.tags.join(', ') : '',
      featured_image: post.featured_image || ''
    });
    setIsEditModalOpen(true);
  };

  const handleSavePost = async () => {
    try {
      if (!formData.title.trim() || !formData.content.trim()) {
        toast({
          title: "Error",
          description: "Please fill in title and content",
          variant: "destructive"
        });
        return;
      }

      const postData = {
        ...formData,
        tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
      };

      if (selectedPost) {
        // Update existing post
        await axios.put(`${API}/posts/${selectedPost.id}`, postData);
        toast({
          title: "Success",
          description: "Post updated successfully"
        });
        setIsEditModalOpen(false);
      } else {
        // Create new post
        await axios.post(`${API}/posts`, postData);
        toast({
          title: "Success",
          description: "Post created successfully"
        });
        setIsCreateModalOpen(false);
      }
      
      loadPosts(); // Reload posts
      setSelectedPost(null);
    } catch (error) {
      console.error('Error saving post:', error);
      toast({
        title: "Error",
        description: error.response?.data?.detail || "Failed to save post",
        variant: "destructive"
      });
    }
  };

  const handleDeletePost = async (postId) => {
    if (window.confirm('Are you sure you want to delete this post?')) {
      try {
        await axios.delete(`${API}/posts/${postId}`);
        toast({
          title: "Success",
          description: "Post deleted successfully"
        });
        loadPosts();
      } catch (error) {
        console.error('Error deleting post:', error);
        toast({
          title: "Error",
          description: "Failed to delete post",
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
  };

  if (isLoading) {
    return (
      <AdminLayout>
        <div className="space-y-6">
          <div className="animate-pulse space-y-6">
            <div className="h-8 bg-gray-200 rounded w-1/4"></div>
            <div className="h-12 bg-gray-200 rounded"></div>
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-48 bg-gray-200 rounded-lg"></div>
              ))}
            </div>
          </div>
        </div>
      </AdminLayout>
    );
  }

  const PostModal = ({ isOpen, onClose, title, isEdit = false }) => (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
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
                placeholder="Post title"
              />
            </div>
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
          </div>

          <div className="space-y-2">
            <Label htmlFor="content">Content *</Label>
            <Textarea
              id="content"
              name="content"
              value={formData.content}
              onChange={handleFormChange}
              placeholder="Write your post content here..."
              className="min-h-[300px]"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="excerpt">Excerpt</Label>
            <Textarea
              id="excerpt"
              name="excerpt"
              value={formData.excerpt}
              onChange={handleFormChange}
              placeholder="Brief description of the post..."
              className="min-h-[80px]"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="category">Category</Label>
              <Input
                id="category"
                name="category"
                value={formData.category}
                onChange={handleFormChange}
                placeholder="Post category"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="tags">Tags</Label>
              <Input
                id="tags"
                name="tags"
                value={formData.tags}
                onChange={handleFormChange}
                placeholder="Tag1, Tag2, Tag3"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="featured_image">Featured Image URL</Label>
            <Input
              id="featured_image"
              name="featured_image"
              value={formData.featured_image}
              onChange={handleFormChange}
              placeholder="https://example.com/image.jpg"
            />
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <Button variant="outline" onClick={() => onClose(false)}>
              <X className="w-4 h-4 mr-2" />
              Cancel
            </Button>
            <Button onClick={handleSavePost}>
              <Save className="w-4 h-4 mr-2" />
              {isEdit ? 'Update Post' : 'Create Post'}
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
            <h1 className="text-2xl font-bold text-gray-900">Posts</h1>
            <p className="text-gray-600">Manage your blog posts and articles</p>
          </div>
          <Button onClick={handleCreatePost} className="flex items-center space-x-2">
            <Plus className="w-4 h-4" />
            <span>New Post</span>
          </Button>
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
                    placeholder="Search posts..."
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>

              {/* Status Filter */}
              <div className="flex items-center space-x-2">
                <Filter className="w-4 h-4 text-gray-400" />
                <select
                  className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <option value="all">All Status</option>
                  <option value="published">Published</option>
                  <option value="draft">Draft</option>
                  <option value="private">Private</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Posts List */}
        <div className="space-y-4">
          {filteredPosts.map(post => (
            <Card key={post.id} className="hover:shadow-md transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900 hover:text-blue-600 cursor-pointer">
                        {post.title}
                      </h3>
                      <Badge className={getStatusColor(post.status)}>
                        {post.status}
                      </Badge>
                    </div>
                    
                    <p className="text-gray-600 mb-3 line-clamp-2">
                      {post.excerpt || (post.content?.substring(0, 150) + '...')}
                    </p>

                    <div className="flex items-center space-x-6 text-sm text-gray-500">
                      <span>By {post.author || 'Unknown'}</span>
                      <span>{new Date(post.created_at || post.createdAt).toLocaleDateString()}</span>
                      {post.category && <span>{post.category}</span>}
                      {post.tags && post.tags.length > 0 && (
                        <div className="flex space-x-2">
                          {post.tags.slice(0, 3).map(tag => (
                            <span key={tag} className="bg-gray-100 px-2 py-1 rounded text-xs">
                              #{tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Featured Image */}
                  {post.featured_image && (
                    <div className="ml-4 flex-shrink-0">
                      <img
                        src={post.featured_image}
                        alt={post.title}
                        className="w-24 h-16 object-cover rounded-lg"
                        onError={(e) => {
                          e.target.style.display = 'none';
                        }}
                      />
                    </div>
                  )}
                </div>

                {/* Actions */}
                <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
                  <div className="flex space-x-2">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="flex items-center space-x-1"
                      onClick={() => handleEditPost(post)}
                    >
                      <Edit className="w-4 h-4" />
                      <span>Edit</span>
                    </Button>
                    <Button variant="outline" size="sm" className="flex items-center space-x-1">
                      <Eye className="w-4 h-4" />
                      <span>View</span>
                    </Button>
                  </div>
                  
                  <div className="flex space-x-2">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="text-red-600 hover:bg-red-50"
                      onClick={() => handleDeletePost(post.id)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                    <Button variant="outline" size="sm">
                      <MoreHorizontal className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredPosts.length === 0 && (
          <Card>
            <CardContent className="p-12 text-center">
              <div className="text-gray-400 mb-4">
                <FileText className="w-12 h-12 mx-auto" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No posts found</h3>
              <p className="text-gray-500 mb-4">
                {searchTerm || statusFilter !== 'all' 
                  ? 'Try adjusting your search or filter criteria'
                  : 'Get started by creating your first post'
                }
              </p>
              <Button onClick={handleCreatePost}>
                <Plus className="w-4 h-4 mr-2" />
                Create Post
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Create Post Modal */}
        <PostModal 
          isOpen={isCreateModalOpen} 
          onClose={setIsCreateModalOpen}
          title="Create New Post"
        />

        {/* Edit Post Modal */}
        <PostModal 
          isOpen={isEditModalOpen} 
          onClose={setIsEditModalOpen}
          title="Edit Post"
          isEdit={true}
        />
      </div>
    </AdminLayout>
  );
};

export default Posts;
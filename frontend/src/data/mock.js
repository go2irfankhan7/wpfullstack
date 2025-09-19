// Mock data for development
export const mockUsers = [
  {
    id: '1',
    name: 'Admin User',
    email: 'admin@cms.com',
    password: 'admin123',
    role: 'admin',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=admin',
    createdAt: '2024-01-01T00:00:00Z'
  },
  {
    id: '2',
    name: 'Editor User',
    email: 'editor@cms.com',
    password: 'editor123',
    role: 'editor',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=editor',
    createdAt: '2024-01-02T00:00:00Z'
  },
  {
    id: '3',
    name: 'Author User',
    email: 'author@cms.com',
    password: 'author123',
    role: 'author',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=author',
    createdAt: '2024-01-03T00:00:00Z'
  }
];

export const mockPosts = [
  {
    id: '1',
    title: 'Welcome to Our CMS',
    content: 'This is the first post in our new CMS system. It demonstrates the post creation and management functionality.',
    excerpt: 'A welcome post showcasing CMS functionality',
    status: 'published',
    authorId: '1',
    author: 'Admin User',
    createdAt: '2024-07-01T10:00:00Z',
    updatedAt: '2024-07-01T10:00:00Z',
    featuredImage: 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=800&h=400&fit=crop',
    tags: ['cms', 'welcome', 'first-post'],
    category: 'General'
  },
  {
    id: '2',
    title: 'Building with Plugins',
    content: 'Our CMS supports a powerful plugin architecture that allows extending functionality both on frontend and backend.',
    excerpt: 'Learn about our plugin system',
    status: 'published',
    authorId: '2',
    author: 'Editor User',
    createdAt: '2024-07-02T14:30:00Z',
    updatedAt: '2024-07-02T14:30:00Z',
    featuredImage: 'https://images.unsplash.com/photo-1558655146-d09347e92766?w=800&h=400&fit=crop',
    tags: ['plugins', 'development', 'architecture'],
    category: 'Development'
  }
];

export const mockPages = [
  {
    id: '1',
    title: 'About Us',
    content: 'Learn more about our company and mission. We are building the next generation CMS platform.',
    slug: 'about-us',
    status: 'published',
    authorId: '1',
    author: 'Admin User',
    createdAt: '2024-07-01T09:00:00Z',
    updatedAt: '2024-07-01T09:00:00Z',
    template: 'default'
  },
  {
    id: '2',
    title: 'Contact',
    content: 'Get in touch with us through our contact form or email.',
    slug: 'contact',
    status: 'draft',
    authorId: '2',
    author: 'Editor User',
    createdAt: '2024-07-02T11:00:00Z',
    updatedAt: '2024-07-02T11:00:00Z',
    template: 'contact'
  }
];

export const mockPlugins = [
  {
    id: 'contact-form-7',
    name: 'Contact Form 7',
    description: 'Simple yet flexible contact form plugin with spam protection and multiple form support.',
    version: '1.0.0',
    author: 'CMS Team',
    category: 'Forms',
    status: 'available',
    price: 'Free',
    downloadUrl: '/plugins/contact-form-7.zip',
    icon: 'https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?w=100&h=100&fit=crop',
    screenshots: [
      'https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?w=600&h=400&fit=crop'
    ],
    features: [
      'Drag & drop form builder',
      'Spam protection',
      'Email notifications',
      'Custom styling options'
    ],
    hooks: {
      'admin_menu': (menu) => {
        menu.push({
          title: 'Contact Forms',
          path: '/admin/contact-forms',
          icon: 'Mail'
        });
        return menu;
      },
      'post_content': (content) => {
        // Replace [contact-form] shortcode with actual form
        return content.replace(/\[contact-form\]/g, '<div class="contact-form-placeholder">Contact Form Here</div>');
      }
    }
  },
  {
    id: 'seo-optimizer',
    name: 'SEO Optimizer',
    description: 'Complete SEO solution with meta tags, sitemap generation, and search engine optimization tools.',
    version: '2.1.0',
    author: 'SEO Experts',
    category: 'SEO',
    status: 'available',
    price: '$29',
    downloadUrl: '/plugins/seo-optimizer.zip',
    icon: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=100&h=100&fit=crop',
    screenshots: [
      'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=400&fit=crop'
    ],
    features: [
      'Meta tag optimization',
      'XML sitemap generation',
      'Social media integration',
      'Analytics tracking'
    ],
    hooks: {
      'admin_menu': (menu) => {
        menu.push({
          title: 'SEO Settings',
          path: '/admin/seo',
          icon: 'TrendingUp'
        });
        return menu;
      }
    }
  },
  {
    id: 'ecommerce-lite',
    name: 'E-commerce Lite',
    description: 'Turn your CMS into an online store with products, shopping cart, and payment integration.',
    version: '1.5.0',
    author: 'Commerce Team',
    category: 'E-commerce',
    status: 'available',
    price: '$99',
    downloadUrl: '/plugins/ecommerce-lite.zip',
    icon: 'https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=100&h=100&fit=crop',
    screenshots: [
      'https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=600&h=400&fit=crop'
    ],
    features: [
      'Product management',
      'Shopping cart',
      'Payment gateway integration',
      'Order management'
    ],
    hooks: {
      'admin_menu': (menu) => {
        menu.push({
          title: 'Products',
          path: '/admin/products',
          icon: 'ShoppingCart'
        });
        return menu;
      }
    }
  },
  {
    id: 'backup-manager',
    name: 'Backup Manager',
    description: 'Automated backup solution for your content, database, and files with cloud storage support.',
    version: '1.2.0',
    author: 'Backup Solutions',
    category: 'Utility',
    status: 'available',
    price: 'Free',
    downloadUrl: '/plugins/backup-manager.zip',
    icon: 'https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=100&h=100&fit=crop',
    screenshots: [
      'https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&h=400&fit=crop'
    ],
    features: [
      'Scheduled backups',
      'Cloud storage integration',
      'One-click restore',
      'Backup verification'
    ],
    hooks: {
      'admin_menu': (menu) => {
        menu.push({
          title: 'Backups',
          path: '/admin/backups',
          icon: 'Download'
        });
        return menu;
      }
    }
  }
];
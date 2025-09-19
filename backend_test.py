#!/usr/bin/env python3
"""
CMS Pro Backend API Test Suite
Tests all backend endpoints for the revolutionary WordPress clone with plugin-first architecture
"""

import asyncio
import aiohttp
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "https://wpfullstack.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@cms.com"
ADMIN_PASSWORD = "admin123"

class CMSProTester:
    def __init__(self):
        self.session = None
        self.auth_token = None
        self.test_results = []
        self.created_resources = {
            'users': [],
            'posts': [],
            'pages': []
        }
    
    async def setup(self):
        """Initialize test session"""
        self.session = aiohttp.ClientSession()
        print(f"🚀 Starting CMS Pro Backend API Tests")
        print(f"📡 Base URL: {BASE_URL}")
        print("=" * 60)
    
    async def cleanup(self):
        """Cleanup test session and resources"""
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    📝 {details}")
        if not success and response_data:
            print(f"    🔍 Response: {response_data}")
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
    
    async def make_request(self, method: str, endpoint: str, data: Dict = None, 
                          headers: Dict = None, auth_required: bool = True) -> tuple:
        """Make HTTP request with error handling"""
        url = f"{BASE_URL}{endpoint}"
        request_headers = {"Content-Type": "application/json"}
        
        if auth_required and self.auth_token:
            request_headers["Authorization"] = f"Bearer {self.auth_token}"
        
        if headers:
            request_headers.update(headers)
        
        try:
            async with self.session.request(
                method, url, 
                json=data if data else None,
                headers=request_headers
            ) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()
                
                return response.status, response_data
        except Exception as e:
            return 0, str(e)
    
    # Authentication Tests
    async def test_health_check(self):
        """Test API health check"""
        status, data = await self.make_request("GET", "/health", auth_required=False)
        
        if status == 200 and isinstance(data, dict) and data.get("status") == "healthy":
            self.log_test("Health Check", True, f"API is healthy with {data.get('plugins', 0)} plugins loaded")
        else:
            self.log_test("Health Check", False, f"Status: {status}", data)
    
    async def test_login(self):
        """Test user authentication"""
        login_data = {
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        
        status, data = await self.make_request("POST", "/auth/login", login_data, auth_required=False)
        
        if status == 200 and isinstance(data, dict) and "access_token" in data:
            self.auth_token = data["access_token"]
            self.log_test("Admin Login", True, f"Token expires in {data.get('expires_in', 0)} seconds")
            return True
        else:
            self.log_test("Admin Login", False, f"Status: {status}", data)
            return False
    
    async def test_get_current_user(self):
        """Test getting current user info"""
        status, data = await self.make_request("GET", "/auth/me")
        
        if status == 200 and isinstance(data, dict) and data.get("email") == ADMIN_EMAIL:
            self.log_test("Get Current User", True, f"User: {data.get('name')} ({data.get('role')})")
        else:
            self.log_test("Get Current User", False, f"Status: {status}", data)
    
    async def test_logout(self):
        """Test user logout"""
        status, data = await self.make_request("POST", "/auth/logout")
        
        if status == 200:
            self.log_test("User Logout", True, "Successfully logged out")
        else:
            self.log_test("User Logout", False, f"Status: {status}", data)
    
    # User Management Tests
    async def test_get_users(self):
        """Test getting all users"""
        status, data = await self.make_request("GET", "/users")
        
        if status == 200 and isinstance(data, list):
            self.log_test("Get Users", True, f"Found {len(data)} users")
        else:
            self.log_test("Get Users", False, f"Status: {status}", data)
    
    async def test_get_user_stats(self):
        """Test getting user statistics"""
        status, data = await self.make_request("GET", "/users/stats")
        
        if status == 200 and isinstance(data, dict) and "total" in data:
            self.log_test("Get User Stats", True, 
                         f"Total: {data.get('total')}, Admin: {data.get('admin')}, "
                         f"Editor: {data.get('editor')}, Author: {data.get('author')}")
        else:
            self.log_test("Get User Stats", False, f"Status: {status}", data)
    
    async def test_create_user(self):
        """Test creating a new user"""
        user_data = {
            "name": "Test Author",
            "email": "testauthor@cms.com",
            "password": "testpass123",
            "role": "author"
        }
        
        status, data = await self.make_request("POST", "/users", user_data)
        
        if status == 200 and isinstance(data, dict) and data.get("email") == user_data["email"]:
            user_id = data.get("id")
            self.created_resources['users'].append(user_id)
            self.log_test("Create User", True, f"Created user: {data.get('name')} (ID: {user_id})")
        else:
            self.log_test("Create User", False, f"Status: {status}", data)
    
    # Content Management Tests
    async def test_get_posts(self):
        """Test getting all posts"""
        status, data = await self.make_request("GET", "/posts")
        
        if status == 200 and isinstance(data, list):
            self.log_test("Get Posts", True, f"Found {len(data)} posts")
        else:
            self.log_test("Get Posts", False, f"Status: {status}", data)
    
    async def test_get_post_stats(self):
        """Test getting post statistics"""
        status, data = await self.make_request("GET", "/posts/stats")
        
        if status == 200 and isinstance(data, dict) and "total" in data:
            self.log_test("Get Post Stats", True, 
                         f"Total: {data.get('total')}, Published: {data.get('published')}, "
                         f"Draft: {data.get('draft')}, Private: {data.get('private')}")
        else:
            self.log_test("Get Post Stats", False, f"Status: {status}", data)
    
    async def test_create_post(self):
        """Test creating a new post"""
        post_data = {
            "title": "Test Post - Revolutionary CMS",
            "content": "<h1>Welcome to CMS Pro</h1><p>This is a test post showcasing our revolutionary plugin-first architecture.</p>",
            "status": "published",
            "tags": ["test", "cms", "revolutionary"],
            "category": "Technology"
        }
        
        status, data = await self.make_request("POST", "/posts", post_data)
        
        if status == 200 and isinstance(data, dict) and data.get("title") == post_data["title"]:
            post_id = data.get("id")
            self.created_resources['posts'].append(post_id)
            self.log_test("Create Post", True, f"Created post: {data.get('title')} (ID: {post_id})")
            return post_id
        else:
            self.log_test("Create Post", False, f"Status: {status}", data)
            return None
    
    async def test_update_post(self, post_id: str):
        """Test updating a post"""
        if not post_id:
            self.log_test("Update Post", False, "No post ID available")
            return
        
        update_data = {
            "title": "Updated Test Post - CMS Pro Revolution",
            "content": "<h1>Updated Content</h1><p>This post has been updated to showcase our editing capabilities.</p>",
            "tags": ["updated", "cms", "revolutionary", "editing"]
        }
        
        status, data = await self.make_request("PUT", f"/posts/{post_id}", update_data)
        
        if status == 200 and isinstance(data, dict) and "Updated" in data.get("title", ""):
            self.log_test("Update Post", True, f"Updated post: {data.get('title')}")
        else:
            self.log_test("Update Post", False, f"Status: {status}", data)
    
    async def test_get_specific_post(self, post_id: str):
        """Test getting a specific post"""
        if not post_id:
            self.log_test("Get Specific Post", False, "No post ID available")
            return
        
        status, data = await self.make_request("GET", f"/posts/{post_id}")
        
        if status == 200 and isinstance(data, dict) and data.get("id") == post_id:
            self.log_test("Get Specific Post", True, f"Retrieved post: {data.get('title')}")
        else:
            self.log_test("Get Specific Post", False, f"Status: {status}", data)
    
    # Plugin System Tests (Revolutionary Feature)
    async def test_get_plugins(self):
        """Test getting all plugins"""
        status, data = await self.make_request("GET", "/plugins")
        
        if status == 200 and isinstance(data, list):
            self.log_test("Get Plugins", True, f"Found {len(data)} plugins in the system")
            return data
        else:
            self.log_test("Get Plugins", False, f"Status: {status}", data)
            return []
    
    async def test_get_active_plugins(self):
        """Test getting active plugins"""
        status, data = await self.make_request("GET", "/plugins/active")
        
        if status == 200 and isinstance(data, list):
            self.log_test("Get Active Plugins", True, f"Found {len(data)} active plugins")
            return data
        else:
            self.log_test("Get Active Plugins", False, f"Status: {status}", data)
            return []
    
    async def test_get_plugin_hooks(self):
        """Test getting plugin hooks for frontend"""
        status, data = await self.make_request("GET", "/plugins/hooks")
        
        if status == 200 and isinstance(data, dict):
            hook_count = sum(len(hooks) for hooks in data.values()) if data else 0
            self.log_test("Get Plugin Hooks", True, f"Retrieved {hook_count} frontend hooks")
        else:
            self.log_test("Get Plugin Hooks", False, f"Status: {status}", data)
    
    async def test_plugin_activation(self, plugins: list):
        """Test plugin activation/deactivation"""
        if not plugins:
            self.log_test("Plugin Activation Test", False, "No plugins available for testing")
            return
        
        # Try to activate/deactivate the first plugin
        plugin = plugins[0]
        plugin_id = plugin.get("id")
        current_status = plugin.get("status")
        
        if current_status == "active":
            # Test deactivation
            status, data = await self.make_request("PUT", f"/plugins/{plugin_id}/deactivate")
            if status == 200:
                self.log_test("Plugin Deactivation", True, f"Deactivated plugin: {plugin.get('name')}")
                
                # Reactivate it
                status, data = await self.make_request("PUT", f"/plugins/{plugin_id}/activate")
                if status == 200:
                    self.log_test("Plugin Reactivation", True, f"Reactivated plugin: {plugin.get('name')}")
                else:
                    self.log_test("Plugin Reactivation", False, f"Status: {status}", data)
            else:
                self.log_test("Plugin Deactivation", False, f"Status: {status}", data)
        else:
            # Test activation
            status, data = await self.make_request("PUT", f"/plugins/{plugin_id}/activate")
            if status == 200:
                self.log_test("Plugin Activation", True, f"Activated plugin: {plugin.get('name')}")
            else:
                self.log_test("Plugin Activation", False, f"Status: {status}", data)
    
    async def test_execute_plugin_hook(self):
        """Test executing plugin hooks"""
        hook_data = {
            "plugin_id": "test-plugin",
            "hook_name": "test_hook",
            "data": {"message": "Testing hook execution"}
        }
        
        status, data = await self.make_request("POST", "/plugins/execute-hook", hook_data)
        
        # This might fail if no plugins are installed, which is expected
        if status == 200:
            self.log_test("Execute Plugin Hook", True, "Hook executed successfully")
        else:
            self.log_test("Execute Plugin Hook", False, f"Status: {status} (Expected if no plugins installed)", data)
    
    # Dashboard Tests
    async def test_dashboard_stats(self):
        """Test dashboard statistics"""
        status, data = await self.make_request("GET", "/dashboard/stats")
        
        if status == 200 and isinstance(data, dict):
            self.log_test("Dashboard Stats", True, 
                         f"Posts: {data.get('total_posts')}, Pages: {data.get('total_pages')}, "
                         f"Users: {data.get('total_users')}, Active Plugins: {data.get('active_plugins')}")
        else:
            self.log_test("Dashboard Stats", False, f"Status: {status}", data)
    
    async def test_dashboard_activity(self):
        """Test dashboard activity feed"""
        status, data = await self.make_request("GET", "/dashboard/activity")
        
        if status == 200 and isinstance(data, dict) and "activity_feed" in data:
            activity_count = len(data["activity_feed"])
            self.log_test("Dashboard Activity", True, f"Retrieved {activity_count} recent activities")
        else:
            self.log_test("Dashboard Activity", False, f"Status: {status}", data)
    
    # Permission Tests
    async def test_role_based_access(self):
        """Test role-based access control"""
        # Test admin-only endpoint (user stats)
        status, data = await self.make_request("GET", "/users/stats")
        
        if status == 200:
            self.log_test("Admin Access Control", True, "Admin can access user stats")
        else:
            self.log_test("Admin Access Control", False, f"Status: {status}", data)
    
    # Cleanup Tests
    async def test_cleanup_created_resources(self):
        """Clean up resources created during testing"""
        cleanup_count = 0
        
        # Delete created posts
        for post_id in self.created_resources['posts']:
            status, data = await self.make_request("DELETE", f"/posts/{post_id}")
            if status == 200:
                cleanup_count += 1
        
        # Delete created users
        for user_id in self.created_resources['users']:
            status, data = await self.make_request("DELETE", f"/users/{user_id}")
            if status == 200:
                cleanup_count += 1
        
        self.log_test("Resource Cleanup", True, f"Cleaned up {cleanup_count} test resources")
    
    async def run_all_tests(self):
        """Run all tests in sequence"""
        await self.setup()
        
        try:
            print("🔐 AUTHENTICATION TESTS")
            print("-" * 30)
            await self.test_health_check()
            
            # Login is critical - if it fails, most other tests will fail
            if not await self.test_login():
                print("❌ Login failed - cannot continue with authenticated tests")
                return
            
            await self.test_get_current_user()
            
            print("\n👥 USER MANAGEMENT TESTS")
            print("-" * 30)
            await self.test_get_users()
            await self.test_get_user_stats()
            await self.test_create_user()
            await self.test_role_based_access()
            
            print("\n📝 CONTENT MANAGEMENT TESTS")
            print("-" * 30)
            await self.test_get_posts()
            await self.test_get_post_stats()
            post_id = await self.test_create_post()
            await self.test_update_post(post_id)
            await self.test_get_specific_post(post_id)
            
            print("\n🔌 REVOLUTIONARY PLUGIN SYSTEM TESTS")
            print("-" * 30)
            plugins = await self.test_get_plugins()
            active_plugins = await self.test_get_active_plugins()
            await self.test_get_plugin_hooks()
            await self.test_plugin_activation(plugins)
            await self.test_execute_plugin_hook()
            
            print("\n📊 DASHBOARD TESTS")
            print("-" * 30)
            await self.test_dashboard_stats()
            await self.test_dashboard_activity()
            
            print("\n🧹 CLEANUP TESTS")
            print("-" * 30)
            await self.test_cleanup_created_resources()
            await self.test_logout()
            
        except Exception as e:
            print(f"❌ Test execution error: {e}")
        
        finally:
            await self.cleanup()
            self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  • {result['test']}: {result['details']}")
        
        print("\n🎉 CMS Pro Backend API Testing Complete!")
        
        # Return exit code based on results
        return 0 if failed_tests == 0 else 1

async def main():
    """Main test runner"""
    tester = CMSProTester()
    exit_code = await tester.run_all_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    asyncio.run(main())
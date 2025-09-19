#!/usr/bin/env python3
"""
Quick test to verify the post ID fix
"""

import asyncio
import aiohttp
import json

BASE_URL = "https://wpfullstack.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@cms.com"
ADMIN_PASSWORD = "admin123"

async def test_post_operations():
    async with aiohttp.ClientSession() as session:
        # Login
        login_data = {"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        async with session.post(f"{BASE_URL}/auth/login", json=login_data) as response:
            if response.status != 200:
                print("❌ Login failed")
                return
            
            data = await response.json()
            token = data["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
        
        # Create a post
        post_data = {
            "title": "Test Post Fix",
            "content": "<p>Testing the ID fix</p>",
            "status": "published"
        }
        
        async with session.post(f"{BASE_URL}/posts", json=post_data, headers=headers) as response:
            if response.status != 200:
                print("❌ Post creation failed")
                return
            
            data = await response.json()
            post_id = data["id"]
            print(f"✅ Created post with ID: {post_id}")
        
        # Try to get the post
        async with session.get(f"{BASE_URL}/posts/{post_id}", headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Retrieved post: {data['title']}")
            else:
                print(f"❌ Failed to retrieve post: {response.status}")
                return
        
        # Try to update the post
        update_data = {"title": "Updated Test Post Fix"}
        async with session.put(f"{BASE_URL}/posts/{post_id}", json=update_data, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Updated post: {data['title']}")
            else:
                print(f"❌ Failed to update post: {response.status}")
                return
        
        # Clean up - delete the post
        async with session.delete(f"{BASE_URL}/posts/{post_id}", headers=headers) as response:
            if response.status == 200:
                print("✅ Deleted test post")
            else:
                print(f"❌ Failed to delete post: {response.status}")

if __name__ == "__main__":
    asyncio.run(test_post_operations())
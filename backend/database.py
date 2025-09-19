import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None

db = Database()

async def get_database():
    return db.database

async def connect_to_mongo():
    """Create database connection"""
    try:
        db.client = AsyncIOMotorClient(os.environ['MONGO_URL'])
        db.database = db.client[os.environ['DB_NAME']]
        
        # Test the connection
        await db.database.command("ping")
        logger.info("Connected to MongoDB successfully")
        
        # Create indexes for better performance
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("Disconnected from MongoDB")

async def create_indexes():
    """Create database indexes for performance"""
    try:
        database = await get_database()
        
        # User indexes
        await database.users.create_index("email", unique=True)
        await database.users.create_index("role")
        await database.users.create_index("is_active")
        
        # Post indexes
        await database.posts.create_index("author_id")
        await database.posts.create_index("status")
        await database.posts.create_index("created_at")
        await database.posts.create_index("tags")
        await database.posts.create_index("category")
        await database.posts.create_index([("title", "text"), ("content", "text")])
        
        # Page indexes
        await database.pages.create_index("slug", unique=True)
        await database.pages.create_index("author_id")
        await database.pages.create_index("status")
        
        # Plugin indexes
        await database.plugins.create_index("status")
        await database.plugins.create_index("category")
        await database.plugins.create_index("name", unique=True)
        
        # Media indexes
        await database.media.create_index("uploaded_by")
        await database.media.create_index("content_type")
        await database.media.create_index("created_at")
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.warning(f"Error creating indexes: {e}")

# Database operations helper functions
async def get_collection(collection_name: str):
    """Get a database collection"""
    database = await get_database()
    return database[collection_name]

async def insert_document(collection_name: str, document: dict) -> str:
    """Insert a document and return its ID"""
    collection = await get_collection(collection_name)
    
    # Add timestamps
    document["created_at"] = datetime.utcnow()
    document["updated_at"] = datetime.utcnow()
    
    result = await collection.insert_one(document)
    return str(result.inserted_id)

async def find_documents(
    collection_name: str,
    filter_dict: dict = None,
    sort: List[tuple] = None,
    limit: int = None,
    skip: int = 0
) -> List[dict]:
    """Find documents with optional filtering, sorting, and pagination"""
    collection = await get_collection(collection_name)
    
    cursor = collection.find(filter_dict or {})
    
    if sort:
        cursor = cursor.sort(sort)
    
    if skip > 0:
        cursor = cursor.skip(skip)
        
    if limit:
        cursor = cursor.limit(limit)
    
    documents = await cursor.to_list(length=None)
    
    # Convert ObjectId to string for JSON serialization
    for doc in documents:
        if "_id" in doc:
            doc["id"] = str(doc["_id"])
    
    return documents

async def find_document(collection_name: str, filter_dict: dict) -> Optional[dict]:
    """Find a single document"""
    collection = await get_collection(collection_name)
    document = await collection.find_one(filter_dict)
    
    if document and "_id" in document:
        document["id"] = str(document["_id"])
    
    return document

async def update_document(
    collection_name: str,
    filter_dict: dict,
    update_dict: dict,
    upsert: bool = False
) -> bool:
    """Update a document"""
    collection = await get_collection(collection_name)
    
    # Add updated timestamp
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await collection.update_one(
        filter_dict,
        {"$set": update_dict},
        upsert=upsert
    )
    
    return result.modified_count > 0 or (upsert and result.upserted_id)

async def delete_document(collection_name: str, filter_dict: dict) -> bool:
    """Delete a document"""
    collection = await get_collection(collection_name)
    result = await collection.delete_one(filter_dict)
    return result.deleted_count > 0

async def count_documents(collection_name: str, filter_dict: dict = None) -> int:
    """Count documents matching filter"""
    collection = await get_collection(collection_name)
    return await collection.count_documents(filter_dict or {})
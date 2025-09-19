from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path

# Import our modules
from database import connect_to_mongo, close_mongo_connection
from plugin_system import plugin_manager
from seed_data import seed_database

# Import route modules
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes.content_routes import router as content_router
from routes.plugin_routes import router as plugin_router
from routes.dashboard_routes import router as dashboard_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the main app
app = FastAPI(
    title="CMS Pro API",
    description="A revolutionary plugin-based content management system",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check endpoint
@api_router.get("/")
async def root():
    return {
        "message": "CMS Pro API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "plugins": len(plugin_manager.loaded_plugins)
    }

# Include all routers
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(content_router)
api_router.include_router(plugin_router)
api_router.include_router(dashboard_router)

# Include the main router in the app
app.include_router(api_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    try:
        logger.info("Starting CMS Pro API...")
        
        # Connect to MongoDB
        await connect_to_mongo()
        
        # Seed database with initial data
        await seed_database()
        
        # Initialize plugin system
        await plugin_manager.initialize()
        
        logger.info("CMS Pro API started successfully!")
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    try:
        logger.info("Shutting down CMS Pro API...")
        await close_mongo_connection()
        logger.info("CMS Pro API shut down successfully!")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

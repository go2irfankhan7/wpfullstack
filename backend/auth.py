import os
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from models import User, UserResponse, TokenData, UserRole
from database import find_document, update_document
import logging

logger = logging.getLogger(__name__)

# Security configurations
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate user by email and password"""
    user_doc = await find_document("users", {"email": email, "is_active": True})
    
    if not user_doc:
        return None
    
    if not verify_password(password, user_doc["password_hash"]):
        return None
    
    return User(**user_doc)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
        token_data = TokenData(user_id=user_id)
        
    except jwt.PyJWTError:
        raise credentials_exception
    
    user_doc = await find_document("users", {"_id": token_data.user_id, "is_active": True})
    
    if user_doc is None:
        raise credentials_exception
    
    return User(**user_doc)

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_role(required_role: UserRole):
    """Dependency factory for role-based access control"""
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if required_role == UserRole.ADMIN and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        elif required_role == UserRole.EDITOR and current_user.role not in [UserRole.ADMIN, UserRole.EDITOR]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Editor access required"
            )
        # Author role is default, so no additional check needed
        
        return current_user
    
    return role_checker

# Permission helpers
def has_permission(user: User, required_role: UserRole) -> bool:
    """Check if user has required role permission"""
    if required_role == UserRole.ADMIN:
        return user.role == UserRole.ADMIN
    elif required_role == UserRole.EDITOR:
        return user.role in [UserRole.ADMIN, UserRole.EDITOR]
    else:  # Author or any authenticated user
        return True

async def can_edit_content(current_user: User, author_id: str) -> bool:
    """Check if user can edit specific content"""
    # Admins and editors can edit any content
    if current_user.role in [UserRole.ADMIN, UserRole.EDITOR]:
        return True
    
    # Authors can only edit their own content
    return current_user.id == author_id
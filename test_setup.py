#!/usr/bin/env python3
"""
Simple test to verify our environment setup is working correctly.
Run this file to check if all dependencies are installed properly.
"""

def test_imports():
    """Test that all required packages can be imported"""
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
        
        import uvicorn
        print("✅ Uvicorn imported successfully")
        
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
        
        import redis
        print("✅ Redis imported successfully")
        
        import pydantic
        print("✅ Pydantic imported successfully")
        
        import pytest
        print("✅ Pytest imported successfully")
        
        print("\n🎉 All dependencies imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test that configuration can be loaded"""
    try:
        from app.config import settings
        print(f"✅ Configuration loaded successfully")
        print(f"   Environment: {settings.ENVIRONMENT}")
        print(f"   Database URL: {settings.DATABASE_URL}")
        print(f"   Redis URL: {settings.REDIS_URL}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing environment setup...\n")
    
    imports_ok = test_imports()
    config_ok = test_config()
    
    if imports_ok and config_ok:
        print("\n✅ Environment setup complete! Ready to proceed to Step 2.")
    else:
        print("\n❌ Environment setup failed. Please check the errors above.")
#!/usr/bin/env python3
"""
Test our FastAPI application
"""

def test_api_imports():
    """Test that API components can be imported"""
    try:
        from app.main import app
        from app.api.trades import router
        print("✅ API components imported successfully")
        return True
    except Exception as e:
        print(f"❌ API import error: {e}")
        return False

def test_app_creation():
    """Test that FastAPI app can be created"""
    try:
        from app.main import app
        
        # Check that app is a FastAPI instance
        from fastapi import FastAPI
        assert isinstance(app, FastAPI)
        
        print("✅ FastAPI app created successfully")
        print(f"   Title: {app.title}")
        print(f"   Version: {app.version}")
        
        return True
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def test_routes_registration():
    """Test that routes are properly registered"""
    try:
        from app.main import app
        
        # Get all registered routes
        routes = [route.path for route in app.routes]
        
        expected_routes = ["/", "/health", "/trades/", "/trades/{trade_id}", "/trades/recent", "/trades/simulate-margin"]
        
        for expected_route in expected_routes:
            # Check if route exists (allowing for OpenAPI routes)
            route_exists = any(expected_route in route or route.endswith(expected_route.replace("{trade_id}", "")) for route in routes)
            if not route_exists:
                print(f"❌ Missing route: {expected_route}")
                print(f"   Available routes: {routes}")
                return False
        
        print("✅ All expected routes registered")
        print(f"   Total routes: {len(routes)}")
        
        return True
    except Exception as e:
        print(f"❌ Route registration error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing FastAPI application...\n")
    
    imports_ok = test_api_imports()
    app_ok = test_app_creation()
    routes_ok = test_routes_registration()
    
    if imports_ok and app_ok and routes_ok:
        print("\n✅ Step 4 complete! API is properly configured.")
        print("🔜 Ready to start the development server!")
        print("\nTo test your API:")
        print("1. Run: uvicorn app.main:app --reload")
        print("2. Visit: http://localhost:8000/docs")
    else:
        print("\n❌ Step 4 failed. Please check the errors above.")
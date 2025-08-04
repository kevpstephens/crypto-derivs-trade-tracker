#!/usr/bin/env python3
"""
Test our database models and schemas
"""

def test_trade_model():
    """Test that our Trade model can be imported and used"""
    try:
        from app.models.trade import Trade, TradeSide, TradeStatus
        print("✅ Trade model imported successfully")
        
        # Test enum values
        assert TradeSide.LONG == "long"
        assert TradeSide.SHORT == "short"
        assert TradeStatus.PENDING == "pending"
        print("✅ Enums working correctly")
        
        return True
    except Exception as e:
        print(f"❌ Trade model error: {e}")
        return False

def test_schemas():
    """Test that our Pydantic schemas work"""
    try:
        from app.schemas.trade import TradeCreate, TradeResponse, MarginSimulation
        from app.models.trade import TradeSide
        from decimal import Decimal
        
        # Test TradeCreate schema
        trade_data = TradeCreate(
            symbol="BTC-PERP",
            side=TradeSide.LONG,
            size=Decimal("0.1"),
            price=Decimal("45000.00"),
            leverage=10
        )
        print("✅ TradeCreate schema working")
        
        # Test MarginSimulation schema
        margin_data = MarginSimulation(
            symbol="BTC-PERP",
            side=TradeSide.LONG,
            size=Decimal("0.1"),
            price=Decimal("50000.00"),
            leverage=10
        )
        print("✅ MarginSimulation schema working")
        
        print("✅ All schemas imported and validated successfully")
        return True
        
    except Exception as e:
        print(f"❌ Schema error: {e}")
        return False

def test_database_config():
    """Test database configuration"""
    try:
        from app.database import Base, engine, get_db
        print("✅ Database configuration imported successfully")
        
        # Test that we can get the database URL
        print(f"✅ Database URL configured: {engine.url}")
        
        return True
    except Exception as e:
        print(f"❌ Database config error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing database models and schemas...\n")
    
    model_ok = test_trade_model()
    schema_ok = test_schemas()
    db_ok = test_database_config()
    
    if model_ok and schema_ok and db_ok:
        print("\n✅ Step 2 complete! Database models and schemas are working.")
        print("🔜 Ready for Step 3: Services Layer")
    else:
        print("\n❌ Step 2 failed. Please check the errors above.")
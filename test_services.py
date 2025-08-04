#!/usr/bin/env python3
"""
Test our services layer
"""

def test_service_imports():
    """Test that services can be imported"""
    try:
        from app.services.cache_service import CacheService
        from app.services.trade_service import TradeService
        print("✅ Services imported successfully")
        return True
    except Exception as e:
        print(f"❌ Service import error: {e}")
        return False

def test_margin_calculations():
    """Test margin calculation logic (doesn't require database)"""
    try:
        from app.services.trade_service import TradeService
        from app.schemas.trade import MarginSimulation
        from app.models.trade import TradeSide
        from decimal import Decimal
        
        # Create a mock trade service (we'll pass None for db and cache for now)
        trade_service = TradeService(db=None, cache_service=None)
        
        # Test margin calculation for a long position
        simulation = MarginSimulation(
            symbol="BTC-PERP",
            side=TradeSide.LONG,
            size=Decimal("0.1"),
            price=Decimal("50000.00"),
            leverage=10
        )
        
        result = trade_service.simulate_margin_requirements(simulation)
        
        # Verify calculations
        expected_margin = Decimal("500.00")  # (0.1 * 50000) / 10
        assert result.required_margin == expected_margin
        
        print("✅ Margin calculation working correctly")
        print(f"   Required margin: ${result.required_margin}")
        print(f"   Maintenance margin: ${result.maintenance_margin}")
        print(f"   Liquidation price: ${result.liquidation_price}")
        print(f"   Max loss: ${result.max_loss}")
        
        return True
        
    except Exception as e:
        print(f"❌ Margin calculation error: {e}")
        return False

def test_schema_validation():
    """Test that our schemas validate correctly"""
    try:
        from app.schemas.trade import TradeCreate, MarginSimulation
        from app.models.trade import TradeSide
        from decimal import Decimal
        
        # Test valid trade creation
        valid_trade = TradeCreate(
            symbol="ETH-PERP",
            side=TradeSide.SHORT,
            size=Decimal("1.0"),
            price=Decimal("3000.00"),
            leverage=5
        )
        print("✅ Valid trade schema works")
        
        # Test that validation catches errors
        try:
            invalid_trade = TradeCreate(
                symbol="BTC-PERP",
                side=TradeSide.LONG,
                size=Decimal("-0.1"),  # Negative size should fail
                price=Decimal("45000.00"),
                leverage=10
            )
            print("❌ Validation should have failed for negative size")
            return False
        except Exception:
            print("✅ Schema validation correctly rejects negative size")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing services layer...\n")
    
    imports_ok = test_service_imports()
    margin_ok = test_margin_calculations()
    validation_ok = test_schema_validation()
    
    if imports_ok and margin_ok and validation_ok:
        print("\n✅ Step 3 complete! Services layer is working.")
        print("🔜 Ready for Step 4: API Endpoints")
    else:
        print("\n❌ Step 3 failed. Please check the errors above.")
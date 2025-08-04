from decimal import Decimal

from app.models.trade import TradeSide
from app.schemas.trade import MarginSimulation
from app.services.trade_service import TradeService


class TestTradeService:

    def test_margin_calculation_long_position(self):
        """Test margin calculation for long position"""
        trade_service = TradeService(db=None, cache_service=None)

        simulation = MarginSimulation(
            symbol="BTC-PERP",
            side=TradeSide.LONG,
            size=Decimal("1.0"),
            price=Decimal("50000.00"),
            leverage=10,
        )

        result = trade_service.simulate_margin_requirements(simulation)

        # Position value: 1.0 * 50000 = 50000
        # Required margin: 50000 / 10 = 5000
        assert result.required_margin == Decimal("5000.00")
        assert result.maintenance_margin == Decimal("2500.00")  # 50% of required
        assert result.max_loss == Decimal("5500.00")  # 110% of required margin

        # Liquidation price should be lower for long positions
        assert result.liquidation_price < simulation.price

    def test_margin_calculation_short_position(self):
        """Test margin calculation for short position"""
        trade_service = TradeService(db=None, cache_service=None)

        simulation = MarginSimulation(
            symbol="ETH-PERP",
            side=TradeSide.SHORT,
            size=Decimal("2.0"),
            price=Decimal("3000.00"),
            leverage=5,
        )

        result = trade_service.simulate_margin_requirements(simulation)

        # Position value: 2.0 * 3000 = 6000
        # Required margin: 6000 / 5 = 1200
        assert result.required_margin == Decimal("1200.00")
        assert result.maintenance_margin == Decimal("600.00")

        # Liquidation price should be higher for short positions
        assert result.liquidation_price > simulation.price

    def test_margin_calculation_high_leverage(self):
        """Test margin calculation with high leverage"""
        trade_service = TradeService(db=None, cache_service=None)

        simulation = MarginSimulation(
            symbol="BTC-PERP",
            side=TradeSide.LONG,
            size=Decimal("0.01"),
            price=Decimal("60000.00"),
            leverage=100,
        )

        result = trade_service.simulate_margin_requirements(simulation)

        # Position value: 0.01 * 60000 = 600
        # Required margin: 600 / 100 = 6
        assert result.required_margin == Decimal("6.00")

        # High leverage should result in liquidation price very close to entry price
        price_difference = abs(simulation.price - result.liquidation_price)
        assert price_difference < simulation.price * Decimal("0.02")  # Less than 2%

    def test_margin_calculation_different_symbols(self):
        """Test that margin calculation works for different symbols"""
        trade_service = TradeService(db=None, cache_service=None)

        symbols = ["BTC-PERP", "ETH-PERP", "SOL-PERP", "AVAX-PERP"]

        for symbol in symbols:
            simulation = MarginSimulation(
                symbol=symbol,
                side=TradeSide.LONG,
                size=Decimal("1.0"),
                price=Decimal("1000.00"),
                leverage=10,
            )

            result = trade_service.simulate_margin_requirements(simulation)
            assert result.required_margin == Decimal(
                "100.00"
            )  # Same calculation regardless of symbol

from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from app.models.trade import Trade, TradeStatus
from app.schemas.trade import TradeCreate, TradeResponse, MarginSimulation, MarginResponse
from app.services.cache_service import CacheService

class TradeService:
    def __init__(self, db: Session, cache_service: CacheService):
        self.db = db
        self.cache_service = cache_service

    async def create_trade(self, trade_data: TradeCreate) -> TradeResponse:
        """Create a new trade"""
        db_trade = Trade(
            symbol=trade_data.symbol,
            side=trade_data.side,
            size=trade_data.size,
            price=trade_data.price,
            leverage=trade_data.leverage,
            status=TradeStatus.FILLED  # Simulate immediate fill for MVP
        )
        
        self.db.add(db_trade)
        self.db.commit()
        self.db.refresh(db_trade)
        
        trade_response = TradeResponse.model_validate(db_trade)
        
        # Cache the trade
        await self.cache_service.cache_trade(trade_response)
        await self.cache_service.cache_trade_by_id(trade_response)
        
        return trade_response

    async def get_trade_by_id(self, trade_id: int) -> Optional[TradeResponse]:
        """Get trade by ID (check cache first)"""
        # Try cache first
        cached_trade = await self.cache_service.get_trade_by_id(trade_id)
        if cached_trade:
            return cached_trade
        
        # Fallback to database
        db_trade = self.db.query(Trade).filter(Trade.id == trade_id).first()
        if db_trade:
            trade_response = TradeResponse.model_validate(db_trade)
            # Cache for future requests
            await self.cache_service.cache_trade_by_id(trade_response)
            return trade_response
        
        return None

    async def get_recent_trades(self, limit: int = 20) -> List[TradeResponse]:
        """Get recent trades from cache"""
        return await self.cache_service.get_recent_trades(limit)

    def simulate_margin_requirements(self, simulation: MarginSimulation) -> MarginResponse:
        """Simulate margin requirements for a trade"""
        position_value = simulation.size * simulation.price
        required_margin = position_value / simulation.leverage
        
        # Maintenance margin (typically 50% of initial margin)
        maintenance_margin = required_margin * Decimal("0.5")
        
        # Simple liquidation price calculation - convert everything to Decimal
        leverage_decimal = Decimal(str(simulation.leverage))
        one = Decimal("1")
        fee_buffer = Decimal("0.005")  # 0.5% fee buffer
        
        if simulation.side.value == "long":
            liquidation_price = simulation.price * (one - one/leverage_decimal + fee_buffer)
        else:  # short
            liquidation_price = simulation.price * (one + one/leverage_decimal - fee_buffer)
        
        # Maximum loss (margin + fees)
        max_loss = required_margin * Decimal("1.1")  # Including estimated fees
        
        return MarginResponse(
            required_margin=required_margin,
            maintenance_margin=maintenance_margin,
            liquidation_price=liquidation_price,
            max_loss=max_loss
        )
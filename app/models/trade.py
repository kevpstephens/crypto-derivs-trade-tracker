from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class TradeSide(str, enum.Enum):
    LONG = "long"
    SHORT = "short"

class TradeStatus(str, enum.Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False, index=True)  # e.g., "BTC-PERP"
    side = Column(Enum(TradeSide), nullable=False)
    size = Column(Numeric(18, 8), nullable=False)  # Position size
    price = Column(Numeric(18, 2), nullable=False)  # Entry price
    status = Column(Enum(TradeStatus), default=TradeStatus.PENDING)
    leverage = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.models.trade import TradeSide, TradeStatus


class TradeCreate(BaseModel):
    symbol: str = Field(..., json_schema_extra={"example": "BTC-PERP"})
    side: TradeSide
    size: Decimal = Field(..., gt=0, json_schema_extra={"example": "0.1"})
    price: Decimal = Field(..., gt=0, json_schema_extra={"example": "45000.00"})
    leverage: int = Field(default=1, ge=1, le=100)


class TradeResponse(BaseModel):
    id: int
    symbol: str
    side: TradeSide
    size: Decimal
    price: Decimal
    status: TradeStatus
    leverage: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class MarginSimulation(BaseModel):
    symbol: str
    side: TradeSide
    size: Decimal
    price: Decimal
    leverage: int = Field(ge=1, le=100)


class MarginResponse(BaseModel):
    required_margin: Decimal
    maintenance_margin: Decimal
    liquidation_price: Decimal
    max_loss: Decimal

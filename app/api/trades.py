from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.trade import (
    MarginResponse,
    MarginSimulation,
    TradeCreate,
    TradeResponse,
)
from app.services.cache_service import CacheService
from app.services.trade_service import TradeService

router = APIRouter(prefix="/trades", tags=["trades"])


def get_trade_service(db: Session = Depends(get_db)) -> TradeService:
    cache_service = CacheService()
    return TradeService(db, cache_service)


@router.post("/", response_model=TradeResponse, status_code=201)
async def create_trade(
    trade_data: TradeCreate, trade_service: TradeService = Depends(get_trade_service)
):
    """Create a new crypto derivative trade"""
    try:
        return await trade_service.create_trade(trade_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create trade: {str(e)}")


@router.post("/simulate-margin", response_model=MarginResponse)
async def simulate_margin_requirements(
    simulation: MarginSimulation,
    trade_service: TradeService = Depends(get_trade_service),
):
    """Simulate margin requirements for a potential trade"""
    return trade_service.simulate_margin_requirements(simulation)


@router.get("/recent", response_model=List[TradeResponse])
async def get_recent_trades(
    limit: int = Query(
        default=20, le=100, description="Number of recent trades to return"
    ),
    trade_service: TradeService = Depends(get_trade_service),
):
    """Get recent trades from cache"""
    return await trade_service.get_recent_trades(limit)


@router.get("/{trade_id}", response_model=TradeResponse)
async def get_trade(
    trade_id: int, trade_service: TradeService = Depends(get_trade_service)
):
    """Get a specific trade by ID"""
    trade = await trade_service.get_trade_by_id(trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade

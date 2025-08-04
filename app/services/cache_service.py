import json
from typing import List, Optional

import redis

from app.config import settings
from app.schemas.trade import TradeResponse


class CacheService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.recent_trades_key = "recent_trades"
        self.max_recent_trades = 100

    async def cache_trade(self, trade: TradeResponse) -> None:
        """Cache a trade in Redis"""
        trade_data = trade.model_dump_json()

        # Add to recent trades list (LPUSH adds to front)
        self.redis_client.lpush(self.recent_trades_key, trade_data)

        # Trim list to max size
        self.redis_client.ltrim(self.recent_trades_key, 0, self.max_recent_trades - 1)

        # Set expiration for the key (24 hours)
        self.redis_client.expire(self.recent_trades_key, 24 * 60 * 60)

    async def get_recent_trades(self, limit: int = 20) -> List[TradeResponse]:
        """Get recent trades from Redis"""
        trade_strings = self.redis_client.lrange(self.recent_trades_key, 0, limit - 1)
        trades = []

        for trade_str in trade_strings:
            try:
                trade_data = json.loads(trade_str)
                trades.append(TradeResponse(**trade_data))
            except (json.JSONDecodeError, ValueError):
                continue

        return trades

    async def get_trade_by_id(self, trade_id: int) -> Optional[TradeResponse]:
        """Get a specific trade from cache"""
        trade_key = f"trade:{trade_id}"
        trade_data = self.redis_client.get(trade_key)

        if trade_data:
            try:
                return TradeResponse(**json.loads(trade_data))
            except (json.JSONDecodeError, ValueError):
                return None
        return None

    async def cache_trade_by_id(self, trade: TradeResponse) -> None:
        """Cache individual trade by ID"""
        trade_key = f"trade:{trade.id}"
        self.redis_client.setex(
            trade_key, 60 * 60, trade.model_dump_json()  # 1 hour expiration
        )

"""
Ticketmaster API client
"""
from datetime import datetime
from decimal import Decimal
from typing import Any
import asyncio

from src.domain.entities.event import Event, PriceTier
from src.domain.entities.search_criteria import SearchCriteria


class TicketmasterClient:
    """Client for Ticketmaster Discovery API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def search_events(self, criteria: SearchCriteria) -> list[Event]:
        """Search for events - returns empty list in demo mode"""
        # Demo mode - returns empty list
        # In production, this would query the real Ticketmaster API
        await asyncio.sleep(0.1)  # Simulate API call
        return []

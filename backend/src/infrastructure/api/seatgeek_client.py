"""
SeatGeek API client
"""
import asyncio
from src.domain.entities.event import Event
from src.domain.entities.search_criteria import SearchCriteria


class SeatGeekClient:
    """Client for SeatGeek API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def search_events(self, criteria: SearchCriteria) -> list[Event]:
        """Search for events - returns empty list in demo mode"""
        await asyncio.sleep(0.1)
        return []


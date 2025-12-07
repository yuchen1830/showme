"""
Search use case - Application layer
Orchestrates the complete search flow
"""
import asyncio
from typing import Protocol

from src.domain.entities.event import Event
from src.domain.entities.search_criteria import SearchCriteria
from src.domain.services.distance_service import DistanceService
from src.domain.services.event_service import EventService


class VendorClient(Protocol):
    """Protocol for vendor API clients"""
    async def search_events(self, criteria: SearchCriteria) -> list[Event]:
        ...


class SearchUseCase:
    """Use case for searching events across multiple vendors"""
    
    def __init__(
        self,
        ticketmaster_client: VendorClient,
        stubhub_client: VendorClient,
        seatgeek_client: VendorClient
    ):
        self.ticketmaster_client = ticketmaster_client
        self.stubhub_client = stubhub_client
        self.seatgeek_client = seatgeek_client
        
        # Domain services
        self.distance_service = DistanceService()
        self.event_service = EventService()
    
    async def execute(
        self,
        criteria: SearchCriteria
    ) -> list[Event]:
        """Execute search across all vendors"""
        # 1. Query all vendors concurrently
        events = await self._query_vendors_concurrently(criteria)
        
        if not events:
            return []
        
        # 2. Deduplicate events (keep cheapest)
        events = self.event_service.deduplicate_events(events)
        
        # 3. Filter by max price if specified
        if criteria.max_price:
            events = self.event_service.filter_by_max_price(events, criteria.max_price)
        
        if not events:
            return []
        
        # 4. Calculate distances from user location
        distances = self._calculate_distances(events, criteria)
        
        # 5. Sort by price then distance
        events = self.event_service.sort_by_price_then_distance(events, distances)
        
        return events
    
    async def _query_vendors_concurrently(
        self,
        criteria: SearchCriteria
    ) -> list[Event]:
        """Query all vendors concurrently"""
        tasks = [
            self._safe_vendor_query(self.ticketmaster_client, criteria),
            self._safe_vendor_query(self.stubhub_client, criteria),
            self._safe_vendor_query(self.seatgeek_client, criteria),
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Flatten results
        all_events = []
        for vendor_events in results:
            all_events.extend(vendor_events)
        
        return all_events
    
    async def _safe_vendor_query(
        self,
        client: VendorClient,
        criteria: SearchCriteria
    ) -> list[Event]:
        """Query vendor with error handling"""
        try:
            return await client.search_events(criteria)
        except Exception as e:
            print(f"Vendor query failed: {e}")
            return []
    
    def _calculate_distances(
        self,
        events: list[Event],
        criteria: SearchCriteria
    ) -> dict[str, float]:
        """Calculate distances from user location"""
        distances = {}
        
        for event in events:
            distance = self.distance_service.calculate_distance(
                lat1=criteria.latitude,
                lon1=criteria.longitude,
                lat2=event.latitude,
                lon2=event.longitude
            )
            distances[event.id] = distance
        
        return distances

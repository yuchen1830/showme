"""
Search use case - Application layer
Orchestrates the complete search flow using AI agents
"""
from typing import Protocol

from src.domain.entities.event import Event
from src.domain.entities.search_criteria import SearchCriteria
from src.domain.services.distance_service import DistanceService
from src.domain.services.event_service import EventService


class AgentClient(Protocol):
    """Protocol for agent-based search client"""
    async def search_events(self, criteria: SearchCriteria) -> list[Event]:
        ...


class SearchUseCase:
    """Use case for searching events using AI agent orchestrator"""
    
    def __init__(self, agent_client: AgentClient):
        self.agent_client = agent_client
        
        # Domain services
        self.distance_service = DistanceService()
        self.event_service = EventService()
    
    async def execute(
        self,
        criteria: SearchCriteria
    ) -> list[Event]:
        """Execute search using AI agents"""
        # 1. Query AI agent orchestrator (searches multiple sites internally)
        events = await self.agent_client.search_events(criteria)
        
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


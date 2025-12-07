"""
Event filtering and sorting service - Domain layer
Pure business logic for event manipulation
"""
from decimal import Decimal

from src.domain.entities.event import Event


class EventService:
    """Service for filtering, sorting, and deduplicating events"""
    
    def filter_by_max_price(
        self,
        events: list[Event],
        max_price: Decimal
    ) -> list[Event]:
        """
        Filter events by maximum price
        
        Args:
            events: List of events to filter
            max_price: Maximum acceptable price
            
        Returns:
            List of events within budget
        """
        return [
            event for event in events
            if event.min_price <= max_price
        ]
    
    def sort_by_price_then_distance(
        self,
        events: list[Event],
        distances: dict[str, float]
    ) -> list[Event]:
        """
        Sort events by price (ascending) then distance (ascending)
        
        Args:
            events: List of events to sort
            distances: Dictionary mapping event IDs to distances in km
            
        Returns:
            Sorted list of events
        """
        return sorted(
            events,
            key=lambda e: (e.min_price, distances.get(e.id, float('inf')))
        )
    
    def deduplicate_events(self, events: list[Event]) -> list[Event]:
        """
        Deduplicate events from multiple vendors
        Keep the cheapest option for each unique event (name + date + venue)
        
        Args:
            events: List of events possibly containing duplicates
            
        Returns:
            Deduplicated list of events
        """
        # Group by (name, date, venue_id)
        event_groups: dict[tuple, list[Event]] = {}
        
        for event in events:
            key = (
                event.name.lower().strip(),
                event.date.date(),  # Compare by date only, ignore time
                event.venue_id
            )
            
            if key not in event_groups:
                event_groups[key] = []
            event_groups[key].append(event)
        
        # Keep cheapest from each group
        deduplicated = []
        for group in event_groups.values():
            # Sort by min_price and keep the cheapest
            cheapest = min(group, key=lambda e: e.min_price)
            deduplicated.append(cheapest)
        
        return deduplicated


"""
Agent Orchestrator Client

This client wraps the AI agent orchestrator to provide ticket search
functionality through browser automation agents.
"""
import uuid
from datetime import datetime
from typing import Optional

from src.domain.entities.event import Event, PriceTier
from src.domain.entities.search_criteria import SearchCriteria


class AgentOrchestratorClient:
    """
    Client that uses AI agents to search for tickets.
    
    This replaces the traditional API clients (Ticketmaster, StubHub, SeatGeek)
    with browser automation agents that actually visit the sites.
    """
    
    async def search_events(self, criteria: SearchCriteria) -> list[Event]:
        """
        Search for events using the AI agent orchestrator.
        
        Note: This can take 2-5 minutes as agents actually browse ticketing sites.
        """
        try:
            # Import the orchestrator (at runtime to avoid circular imports)
            from orchestrator.coordinator import run_ticket_search
            
            # Execute the agent search
            result = await run_ticket_search(
                query=criteria.artist,
                location=criteria.location or "",
                headless=False,  # Show browsers for debugging
            )
            
            # Convert orchestrator result to backend Event format
            return self._convert_to_events(result, criteria)
            
        except Exception as e:
            print(f"[AgentOrchestratorClient] Error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _convert_to_events(self, orchestrator_result, criteria: SearchCriteria) -> list[Event]:
        """
        Convert OrchestratorResult to list of backend Event entities.
        
        The orchestrator returns:
        - events: list of model Event objects
        - ranked_seats: list of Seat objects with AI value scores
        - search_results: dict of site -> SiteSearchResult with raw listings
        """
        from decimal import Decimal
        events = []
        
        # If orchestrator returned events directly, convert them
        if orchestrator_result.events:
            for e in orchestrator_result.events:
                # Create at least one price tier
                price = Decimal(str(e.lowestPrice)) if e.lowestPrice else Decimal("100.00")
                price_tiers = [PriceTier(
                    name="General",
                    min_price=price,
                    max_price=price,
                    currency="USD"
                )]
                
                event = Event(
                    id=e.id,
                    name=e.title,
                    artist=criteria.artist,
                    venue_id=e.venue.id if e.venue else "unknown",
                    venue_name=e.venue.name if e.venue else "Unknown Venue",
                    date=e.date,
                    location=e.venue.address if e.venue else criteria.location,
                    latitude=e.venue.lat if e.venue else 0.0,
                    longitude=e.venue.lng if e.venue else 0.0,
                    price_tiers=price_tiers,
                    vendor=e.vendorSource,
                    vendor_url=""
                )
                events.append(event)
        
        # Also check search_results for raw listings and create events from them
        if orchestrator_result.search_results:
            for site_name, site_result in orchestrator_result.search_results.items():
                if site_result.listings:
                    # Create price tiers from listings
                    price_tiers = []
                    for listing in site_result.listings[:5]:  # Top 5 listings
                        if listing.price_per_ticket > 0:
                            price = Decimal(str(listing.price_per_ticket))
                            total = Decimal(str(listing.total_price)) if listing.total_price else price
                            price_tiers.append(PriceTier(
                                name=f"{listing.section} {listing.row or ''}".strip() or "General",
                                min_price=price,
                                max_price=total,
                                currency="USD"
                            ))
                    
                    # Skip if no valid price tiers
                    if not price_tiers:
                        # Create a placeholder tier
                        price_tiers = [PriceTier(
                            name="Various",
                            min_price=Decimal("0.00"),
                            max_price=Decimal("0.00"),
                            currency="USD"
                        )]
                    
                    # Get venue info from event_info
                    venue_name = "Unknown Venue"
                    if orchestrator_result.event_info and orchestrator_result.event_info.venues:
                        venue_name = orchestrator_result.event_info.venues[0]
                    
                    event = Event(
                        id=str(uuid.uuid4()),
                        name=f"{criteria.artist} ({site_name.title()})",
                        artist=criteria.artist,
                        venue_id=f"{site_name}-venue",
                        venue_name=venue_name,
                        date=datetime.now(),  # Would need to extract from listings
                        location=criteria.location or "",
                        latitude=criteria.latitude or 0.0,
                        longitude=criteria.longitude or 0.0,
                        price_tiers=price_tiers,
                        vendor=site_name,
                        vendor_url=site_result.search_url or ""
                    )
                    events.append(event)
        
        return events


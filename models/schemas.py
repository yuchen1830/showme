"""
Data models for the multi-agent ticket search system.
These schemas match the frontend entities for seamless integration.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class AgentStatus(Enum):
    """Status of an agent's execution."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"  # Some results, but not complete


@dataclass
class Venue:
    """Venue information - matches frontend Venue entity."""
    id: str
    name: str
    address: str
    lat: float = 0.0
    lng: float = 0.0


@dataclass
class Event:
    """Event information - matches frontend Event entity."""
    id: str
    title: str
    date: datetime
    venue: Venue
    lowestPrice: float
    distance: float
    vendorSource: str  # "ticketmaster", "stubhub", "seatgeek", "tickpick"


@dataclass
class Seat:
    """Seat/ticket information - matches frontend Seat entity."""
    id: str
    section: str
    row: str
    seatNumber: str
    price: float
    available: bool
    aiValueScore: int  # 0-100, calculated by ValueAnalyzerAgent

    # Additional fields for internal use
    fees: float = 0.0
    url: str = ""
    source: str = ""  # Which site this came from


@dataclass
class TicketListing:
    """Raw ticket listing from a site search agent."""
    source: str  # "ticketmaster", "stubhub", etc.
    section: str
    row: Optional[str] = None
    seat_numbers: Optional[str] = None
    quantity: int = 1
    price_per_ticket: float = 0.0
    fees_per_ticket: float = 0.0
    total_price: float = 0.0
    url: str = ""
    is_verified: bool = False
    notes: str = ""


@dataclass
class SiteSearchResult:
    """Result from a single site search agent."""
    site_name: str
    status: AgentStatus
    listings: list[TicketListing] = field(default_factory=list)
    error_message: Optional[str] = None
    search_url: str = ""
    screenshots: list[str] = field(default_factory=list)


@dataclass
class SectionQuality:
    """Quality rating for a venue section."""
    section_name: str
    quality_score: float  # 1-10
    notes: str = ""


@dataclass
class VenueIntel:
    """Intelligence gathered about a venue by VenueIntelAgent."""
    venue_name: str
    city: str
    sections: list[SectionQuality] = field(default_factory=list)
    best_value_sections: list[str] = field(default_factory=list)
    avoid_sections: list[str] = field(default_factory=list)
    seating_chart_url: Optional[str] = None
    tips: list[str] = field(default_factory=list)

    def get_section_quality(self, section_name: str) -> float:
        """Get quality score for a section (default 5.0 if not found)."""
        section_lower = section_name.lower()
        for section in self.sections:
            if section.section_name.lower() in section_lower or section_lower in section.section_name.lower():
                return section.quality_score
        return 5.0  # Default middle quality


@dataclass
class EventInfo:
    """Event information gathered by ResearchAgent."""
    artist_name: str
    event_name: str
    dates: list[datetime] = field(default_factory=list)
    venues: list[str] = field(default_factory=list)
    city: str = ""
    tour_name: Optional[str] = None
    notes: str = ""


@dataclass
class SearchQuery:
    """User's search query - matches frontend SearchCriteria."""
    query: str  # Artist/event name
    location: str  # City or coords
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_price: Optional[float] = None


@dataclass
class OrchestratorResult:
    """Final result from the orchestrator."""
    query: SearchQuery
    event_info: Optional[EventInfo] = None
    venue_intel: Optional[VenueIntel] = None
    search_results: dict[str, SiteSearchResult] = field(default_factory=dict)
    ranked_seats: list[Seat] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def to_frontend_json(self) -> dict:
        """Convert to JSON format expected by frontend."""
        return {
            "events": [
                {
                    "id": e.id,
                    "title": e.title,
                    "date": e.date.isoformat(),
                    "venue": {
                        "id": e.venue.id,
                        "name": e.venue.name,
                        "address": e.venue.address,
                        "lat": e.venue.lat,
                        "lng": e.venue.lng,
                    },
                    "lowestPrice": e.lowestPrice,
                    "distance": e.distance,
                    "vendorSource": e.vendorSource,
                }
                for e in self.events
            ],
            "seats": [
                {
                    "id": s.id,
                    "section": s.section,
                    "row": s.row,
                    "seatNumber": s.seatNumber,
                    "price": s.price,
                    "available": s.available,
                    "aiValueScore": s.aiValueScore,
                }
                for s in self.ranked_seats
            ],
            "errors": self.errors,
        }

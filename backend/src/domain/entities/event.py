"""
Event entity - Domain layer
Pure business logic with no external dependencies
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class PriceTier:
    """Value object representing a price tier for an event"""
    name: str
    min_price: Decimal
    max_price: Decimal
    currency: str
    
    def __post_init__(self):
        """Validate price tier invariants"""
        if self.min_price < 0 or self.max_price < 0:
            raise ValueError("Prices must be non-negative")
        
        if self.min_price > self.max_price:
            raise ValueError("min_price cannot be greater than max_price")


@dataclass
class Event:
    """
    Event entity representing a concert/show
    Aggregates data from multiple ticket vendors
    """
    id: str
    name: str
    artist: str
    venue_id: str
    venue_name: str
    date: datetime
    location: str
    latitude: float
    longitude: float
    price_tiers: list[PriceTier]
    vendor: str
    vendor_url: str
    
    def __post_init__(self):
        """Validate event invariants"""
        if not self.price_tiers:
            raise ValueError("Event must have at least one price tier")
        
        # Validate coordinates
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Invalid latitude: {self.latitude}")
        
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Invalid longitude: {self.longitude}")
    
    @property
    def min_price(self) -> Decimal:
        """Get the minimum price across all tiers"""
        return min(tier.min_price for tier in self.price_tiers)
    
    @property
    def max_price(self) -> Decimal:
        """Get the maximum price across all tiers"""
        return max(tier.max_price for tier in self.price_tiers)


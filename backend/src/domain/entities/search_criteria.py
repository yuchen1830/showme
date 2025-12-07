"""
SearchCriteria entity - Domain layer
Represents user's search parameters for finding events
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class SearchCriteria:
    """Value object representing user search criteria"""
    artist: str
    location: str
    latitude: float
    longitude: float
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_price: Optional[Decimal] = None
    
    def __post_init__(self):
        """Validate search criteria invariants"""
        # Validate artist
        if not self.artist or not self.artist.strip():
            raise ValueError("Artist name cannot be empty")
        
        # Validate coordinates
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Invalid latitude: {self.latitude}")
        
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Invalid longitude: {self.longitude}")
        
        # Validate dates
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("end_date cannot be before start_date")
        
        # Validate price
        if self.max_price is not None and self.max_price <= 0:
            raise ValueError("max_price must be positive")


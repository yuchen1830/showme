"""
Venue and SeatSection entities - Domain layer
Represents concert venues and their seating arrangements
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class SeatSection:
    """Entity representing a section of seats in a venue"""
    id: str
    name: str
    row_start: int
    row_end: int
    price: Decimal
    currency: str
    value_score: Optional[int] = None  # AI-calculated value score (0-100)
    
    def __post_init__(self):
        """Validate seat section invariants"""
        if self.price < 0:
            raise ValueError("Price must be non-negative")
        
        if self.row_end < self.row_start:
            raise ValueError("row_end must be greater than or equal to row_start")
        
        if self.value_score is not None:
            if not 0 <= self.value_score <= 100:
                raise ValueError("value_score must be between 0 and 100")


@dataclass
class Venue:
    """Entity representing a concert venue"""
    id: str
    name: str
    location: str
    latitude: float
    longitude: float
    capacity: int
    sections: list[SeatSection]
    
    def __post_init__(self):
        """Validate venue invariants"""
        # Validate coordinates
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Invalid latitude: {self.latitude}")
        
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Invalid longitude: {self.longitude}")
        
        # Validate capacity
        if self.capacity <= 0:
            raise ValueError("Capacity must be positive")


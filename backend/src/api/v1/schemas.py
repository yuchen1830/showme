"""
Pydantic schemas for API requests/responses
"""
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Request schema for event search"""
    artist: str = Field(..., min_length=1, max_length=200, description="Artist name")
    location: str = Field(..., description="Location (city, state)")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    start_date: datetime | None = Field(None, description="Start date for events")
    end_date: datetime | None = Field(None, description="End date for events")
    max_price: Decimal | None = Field(None, gt=0, description="Maximum ticket price")


class PriceTierResponse(BaseModel):
    """Price tier in response"""
    name: str
    min_price: Decimal
    max_price: Decimal
    currency: str


class EventResponse(BaseModel):
    """Event in response"""
    id: str
    name: str
    artist: str
    venue_name: str
    date: datetime
    location: str
    latitude: float
    longitude: float
    price_tiers: list[PriceTierResponse]
    min_price: Decimal
    max_price: Decimal
    vendor: str
    vendor_url: str


class SearchResponse(BaseModel):
    """Response schema for event search"""
    events: list[EventResponse]
    total: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime

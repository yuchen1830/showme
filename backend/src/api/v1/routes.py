"""
API v1 routes
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_search_use_case
from src.api.v1.schemas import SearchRequest, SearchResponse, EventResponse, PriceTierResponse, HealthResponse
from src.application.use_cases.search_use_case import SearchUseCase
from src.domain.entities.search_criteria import SearchCriteria


router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns service status and version
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow()
    )


@router.post("/search", response_model=SearchResponse)
async def search_events(
    request: SearchRequest,
    use_case: SearchUseCase = Depends(get_search_use_case)
):
    """
    Search for events across multiple ticket vendors
    
    - Queries Ticketmaster, StubHub, and SeatGeek concurrently
    - Deduplicates results (keeps cheapest option)
    - Filters by max price (if specified)
    - Sorts by price (ascending), then distance (ascending)
    
    Performance target: p95 < 2s
    """
    try:
        # Convert request to domain entity
        criteria = SearchCriteria(
            artist=request.artist,
            location=request.location,
            latitude=request.latitude,
            longitude=request.longitude,
            start_date=request.start_date,
            end_date=request.end_date,
            max_price=request.max_price
        )
        
        # Execute search
        events = await use_case.execute(criteria)
        
        # Convert to response format
        event_responses = [
            EventResponse(
                id=event.id,
                name=event.name,
                artist=event.artist,
                venue_name=event.venue_name,
                date=event.date,
                location=event.location,
                latitude=event.latitude,
                longitude=event.longitude,
                price_tiers=[
                    PriceTierResponse(
                        name=tier.name,
                        min_price=tier.min_price,
                        max_price=tier.max_price,
                        currency=tier.currency
                    )
                    for tier in event.price_tiers
                ],
                min_price=event.min_price,
                max_price=event.max_price,
                vendor=event.vendor,
                vendor_url=event.vendor_url
            )
            for event in events
        ]
        
        return SearchResponse(
            events=event_responses,
            total=len(event_responses)
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

"""
FastAPI dependencies
"""
from functools import lru_cache
import os

from src.application.use_cases.search_use_case import SearchUseCase
from src.infrastructure.api.ticketmaster_client import TicketmasterClient
from src.infrastructure.api.stubhub_client import StubHubClient
from src.infrastructure.api.seatgeek_client import SeatGeekClient


@lru_cache()
def get_settings():
    """Get application settings"""
    return {
        "ticketmaster_api_key": os.getenv("TICKETMASTER_API_KEY", "demo_key"),
        "stubhub_api_key": os.getenv("STUBHUB_API_KEY", "demo_key"),
        "seatgeek_api_key": os.getenv("SEATGEEK_API_KEY", "demo_key"),
    }


def get_search_use_case() -> SearchUseCase:
    """Dependency for search use case"""
    settings = get_settings()
    
    return SearchUseCase(
        ticketmaster_client=TicketmasterClient(settings["ticketmaster_api_key"]),
        stubhub_client=StubHubClient(settings["stubhub_api_key"]),
        seatgeek_client=SeatGeekClient(settings["seatgeek_api_key"])
    )


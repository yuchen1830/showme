"""
ValueAnalyzerAgent: Calculates aiValueScore for each ticket based on price and seat quality.
This is a pure Python agent - no browser needed, just computation.
"""

import statistics
import uuid
from typing import Optional

from models import (
    Seat,
    TicketListing,
    SiteSearchResult,
    VenueIntel,
    Event,
    Venue,
    EventInfo,
)


class ValueAnalyzerAgent:
    """
    Analyzes ticket listings and calculates value scores.
    No browser needed - this is pure computation.
    """

    def __init__(self):
        self.name = "ValueAnalyzerAgent"

    def analyze(
        self,
        search_results: dict[str, SiteSearchResult],
        venue_intel: Optional[VenueIntel] = None,
        event_info: Optional[EventInfo] = None,
    ) -> tuple[list[Seat], list[Event]]:
        """
        Analyze all ticket listings and calculate value scores.

        Args:
            search_results: Dict of site_name -> SiteSearchResult
            venue_intel: Venue quality information (optional)
            event_info: Event details (optional)

        Returns:
            Tuple of (ranked_seats, events)
        """
        print(f"[{self.name}] Analyzing {sum(len(r.listings) for r in search_results.values())} listings...")

        # Collect all listings
        all_listings = []
        for site_name, result in search_results.items():
            all_listings.extend(result.listings)

        if not all_listings:
            print(f"[{self.name}] No listings to analyze")
            return [], []

        # Calculate median price for normalization
        prices = [l.total_price for l in all_listings if l.total_price > 0]
        median_price = statistics.median(prices) if prices else 100.0

        print(f"[{self.name}] Median price: ${median_price:.2f}")

        # Calculate value score for each listing
        scored_seats = []
        for listing in all_listings:
            seat = self._create_seat_from_listing(listing, venue_intel, median_price)
            scored_seats.append(seat)

        # Sort by value score (highest first)
        scored_seats.sort(key=lambda s: s.aiValueScore, reverse=True)

        # Create events for frontend
        events = self._create_events(search_results, event_info)

        print(f"[{self.name}] Analysis complete. Top score: {scored_seats[0].aiValueScore if scored_seats else 0}")

        return scored_seats, events

    def _create_seat_from_listing(
        self,
        listing: TicketListing,
        venue_intel: Optional[VenueIntel],
        median_price: float,
    ) -> Seat:
        """Convert a TicketListing to a Seat with aiValueScore."""

        # Get section quality (1-10)
        if venue_intel:
            section_quality = venue_intel.get_section_quality(listing.section)
        else:
            section_quality = self._estimate_section_quality(listing.section)

        # Calculate value score (0-100)
        value_score = self._calculate_value_score(
            price=listing.total_price or listing.price_per_ticket,
            section_quality=section_quality,
            median_price=median_price,
            is_verified=listing.is_verified,
        )

        return Seat(
            id=str(uuid.uuid4()),
            section=listing.section,
            row=listing.row or "",
            seatNumber=listing.seat_numbers or "",
            price=listing.total_price or listing.price_per_ticket,
            available=True,
            aiValueScore=value_score,
            fees=listing.fees_per_ticket,
            url=listing.url,
            source=listing.source,
        )

    def _calculate_value_score(
        self,
        price: float,
        section_quality: float,
        median_price: float,
        is_verified: bool = False,
    ) -> int:
        """
        Calculate aiValueScore (0-100) for a seat.

        Formula: score = (quality / price_ratio) * multiplier
        Higher quality and lower price = higher score

        Args:
            price: Total ticket price
            section_quality: Quality rating 1-10
            median_price: Median price across all listings
            is_verified: Whether seller is verified (bonus)

        Returns:
            aiValueScore between 0-100
        """
        if price <= 0:
            return 50  # Default for unknown prices

        # Calculate price ratio (how expensive relative to median)
        price_ratio = price / median_price

        # Base score: quality * 10 gives us 10-100 range
        # Then adjust by price ratio
        # If price_ratio < 1 (cheaper than median), score goes up
        # If price_ratio > 1 (more expensive), score goes down

        raw_score = (section_quality * 10) / price_ratio

        # Apply verified bonus (10% boost)
        if is_verified:
            raw_score *= 1.10

        # Apply diminishing returns for very high scores
        # and floor for very low scores
        final_score = int(min(100, max(0, raw_score)))

        return final_score

    def _estimate_section_quality(self, section_name: str) -> float:
        """Estimate section quality when venue intel is unavailable."""
        section_lower = section_name.lower()

        # Common section quality mappings
        quality_map = {
            "floor": 9.0,
            "pit": 9.5,
            "vip": 9.0,
            "orchestra": 8.5,
            "front": 8.5,
            "premium": 8.0,
            "lower": 7.5,
            "club": 7.0,
            "100": 7.5,
            "200": 6.0,
            "mezzanine": 6.5,
            "mezz": 6.5,
            "loge": 6.0,
            "upper": 5.0,
            "300": 5.0,
            "balcony": 4.5,
            "400": 4.0,
            "nosebleed": 3.5,
        }

        for key, quality in quality_map.items():
            if key in section_lower:
                return quality

        # Default middle quality for unknown sections
        return 5.5

    def _create_events(
        self,
        search_results: dict[str, SiteSearchResult],
        event_info: Optional[EventInfo],
    ) -> list[Event]:
        """Create Event objects for the frontend."""
        events = []

        # Create one event per site that returned results
        for site_name, result in search_results.items():
            if not result.listings:
                continue

            # Find the lowest price from this site
            prices = [l.total_price or l.price_per_ticket for l in result.listings if (l.total_price or l.price_per_ticket) > 0]
            lowest_price = min(prices) if prices else 0

            # Create venue
            venue_name = event_info.venues[0] if event_info and event_info.venues else "Venue"
            venue = Venue(
                id=f"venue-{site_name}",
                name=venue_name,
                address=event_info.city if event_info else "",
            )

            # Create event
            from datetime import datetime
            event = Event(
                id=f"event-{site_name}-{uuid.uuid4().hex[:8]}",
                title=event_info.event_name if event_info else "Event",
                date=event_info.dates[0] if event_info and event_info.dates else datetime.now(),
                venue=venue,
                lowestPrice=lowest_price,
                distance=0.0,  # Would need geolocation to calculate
                vendorSource=site_name,
            )
            events.append(event)

        # Sort by lowest price
        events.sort(key=lambda e: e.lowestPrice)

        return events


def analyze_tickets(
    search_results: dict[str, SiteSearchResult],
    venue_intel: Optional[VenueIntel] = None,
    event_info: Optional[EventInfo] = None,
) -> tuple[list[Seat], list[Event]]:
    """Convenience function to analyze tickets."""
    analyzer = ValueAnalyzerAgent()
    return analyzer.analyze(search_results, venue_intel, event_info)

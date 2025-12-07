"""
Quick test to verify all agents can be imported and initialized.
"""

import asyncio
from models import SearchQuery, EventInfo, VenueIntel, TicketListing, SiteSearchResult
from agents import ResearchAgent, SiteSearchAgent, VenueIntelAgent, ValueAnalyzerAgent

def test_imports():
    """Test that all modules import correctly."""
    print("✓ All imports successful")

def test_data_models():
    """Test creating data model instances."""
    query = SearchQuery(query="Test", location="Test City")
    event = EventInfo(artist_name="Test Artist", event_name="Test Event", city="Test")
    listing = TicketListing(source="ticketmaster", section="100", price_per_ticket=50)

    print("✓ Data models working")

def test_agent_creation():
    """Test creating agent instances (without running them)."""
    research = ResearchAgent(headless=True)
    site = SiteSearchAgent("ticketmaster", headless=True)
    venue = VenueIntelAgent(headless=True)
    analyzer = ValueAnalyzerAgent()

    print("✓ All agents can be instantiated")

def test_value_analyzer():
    """Test ValueAnalyzerAgent (doesn't need browser)."""
    analyzer = ValueAnalyzerAgent()

    # Create mock data
    listings = [
        TicketListing(source="test", section="Floor", price_per_ticket=100, total_price=100),
        TicketListing(source="test", section="Upper", price_per_ticket=50, total_price=50),
    ]

    result = SiteSearchResult(site_name="test", status="success", listings=listings)

    seats, events = analyzer.analyze({"test": result})

    assert len(seats) == 2
    assert seats[0].aiValueScore > 0
    assert seats[0].aiValueScore <= 100

    print(f"✓ ValueAnalyzer working - calculated scores: {[s.aiValueScore for s in seats]}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("QUICK VERIFICATION TEST")
    print("="*60 + "\n")

    test_imports()
    test_data_models()
    test_agent_creation()
    test_value_analyzer()

    print("\n" + "="*60)
    print("ALL TESTS PASSED ✓")
    print("="*60)
    print("\nReady to run full search with:")
    print("  python main.py \"Louis CK\" \"San Francisco\"")
    print("\nOr headless mode:")
    print("  python main.py \"Louis CK\" \"San Francisco\" --headless")

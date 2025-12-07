"""
Quick test script - Tests a single agent for faster iteration.
Usage: python3 test_single_agent.py
"""

import asyncio
from models import EventInfo
from agents.site_search import SiteSearchAgent

# Test with TickPick - historically has worked well and shows prices clearly
TEST_SITE = "tickpick"  # Change to: ticketmaster, stubhub, seatgeek, tickpick

# Mock event info (skips ResearchAgent for speed)
TEST_EVENT = EventInfo(
    artist_name="Louis CK",
    event_name="Louis CK",
    city="Stockton",
    venues=["Bob Hope Theatre"],
)

async def test_single_agent():
    """Test a single site agent."""
    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                    QUICK TEST - SINGLE AGENT                         ║
╚══════════════════════════════════════════════════════════════════════╝

Testing: {TEST_SITE.upper()}
Artist: {TEST_EVENT.artist_name}
City: {TEST_EVENT.city}

This should take ~2-3 minutes (vs 9+ for full search)
Watch the browser open and navigate...
""")

    # Create and run the agent
    agent = SiteSearchAgent(site_name=TEST_SITE, headless=False)
    result = await agent.run(TEST_EVENT)

    # Display results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"Status: {result.status}")
    print(f"URL: {result.search_url}")
    print(f"Listings found: {len(result.listings)}")

    if result.error_message:
        print(f"Error: {result.error_message}")

    print("\n" + "-"*70)
    print("TICKET LISTINGS")
    print("-"*70)

    for i, listing in enumerate(result.listings, 1):
        print(f"\n#{i}")
        print(f"  Section: {listing.section}")
        if listing.row:
            print(f"  Row: {listing.row}")
        print(f"  Price: ${listing.price_per_ticket:.2f}")
        print(f"  Quantity: {listing.quantity}")
        if listing.notes:
            print(f"  Notes: {listing.notes}")

    # Check if we got real data
    real_data = any(l.price_per_ticket > 0 for l in result.listings)
    if real_data:
        print("\n" + "="*70)
        print("✓ SUCCESS - Got real pricing data!")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("✗ FAILED - No pricing data extracted (all $0.00)")
        print("Check the browser window to see what happened")
        print("="*70)

if __name__ == "__main__":
    try:
        asyncio.run(test_single_agent())
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
    except Exception as err:
        print(f"\nError: {err}")
        import traceback
        traceback.print_exc()

"""
ShowMe - Multi-Agent Ticket Search Expert
Finds the best VALUE tickets across multiple platforms.

Usage:
    python main.py                          # Interactive mode
    python main.py "Artist Name" "City"     # Direct search
    python main.py --headless               # Run without browser UI
"""

import asyncio
import json
import sys
from datetime import datetime

from dotenv import load_dotenv

from orchestrator import run_ticket_search

load_dotenv()


# ============================================================================
# EXAMPLE SEARCHES - Uncomment one to test
# ============================================================================

# Example 1: Comedy show
DEFAULT_QUERY = "Louis CK"
DEFAULT_LOCATION = "Stockton"

# Example 2: Concert
# DEFAULT_QUERY = "Taylor Swift"
# DEFAULT_LOCATION = "Los Angeles"

# Example 3: Sports
# DEFAULT_QUERY = "Lakers vs Warriors"
# DEFAULT_LOCATION = "Los Angeles"


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================


def print_results(result):
    """Pretty print search results."""
    print("\n" + "=" * 70)
    print("TOP TICKET RECOMMENDATIONS (by Value Score)")
    print("=" * 70)

    if not result.ranked_seats:
        print("\nNo tickets found. Check the errors below.")
    else:
        # Show top 10 seats
        for i, seat in enumerate(result.ranked_seats[:10], 1):
            score_bar = "█" * (seat.aiValueScore // 10) + "░" * (10 - seat.aiValueScore // 10)
            print(f"\n#{i} | Score: {seat.aiValueScore}/100 [{score_bar}]")
            print(f"    Section: {seat.section}")
            if seat.row:
                print(f"    Row: {seat.row}")
            print(f"    Price: ${seat.price:.2f}")
            print(f"    Source: {seat.source}")
            if seat.url:
                print(f"    URL: {seat.url}")

    # Show events by source
    if result.events:
        print("\n" + "-" * 70)
        print("PRICE BY SOURCE")
        print("-" * 70)
        for event in result.events:
            print(f"  {event.vendorSource.upper():15} | Lowest: ${event.lowestPrice:.2f}")

    # Show errors
    if result.errors:
        print("\n" + "-" * 70)
        print("WARNINGS/ERRORS")
        print("-" * 70)
        for error in result.errors:
            print(f"  ⚠ {error}")


def export_json(result, filename=None):
    """Export results to JSON for frontend."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"downloads/results_{timestamp}.json"

    data = result.to_frontend_json()

    with open(filename, "w") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"\nResults exported to: {filename}")
    return filename


# ============================================================================
# MAIN
# ============================================================================


async def main():
    """Main entry point."""
    # Parse command line arguments
    query = DEFAULT_QUERY
    location = DEFAULT_LOCATION
    headless = False
    sites = None  # Use all sites

    # Simple argument parsing
    args = sys.argv[1:]
    if "--headless" in args:
        headless = True
        args.remove("--headless")

    if "--help" in args or "-h" in args:
        print(__doc__)
        print("\nAvailable sites: ticketmaster, stubhub, seatgeek, tickpick, vividseats")
        return

    if len(args) >= 1:
        query = args[0]
    if len(args) >= 2:
        location = args[1]

    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                    SHOWME - TICKET SEARCH EXPERT                     ║
║                  Multi-Agent Value Analysis System                   ║
╚══════════════════════════════════════════════════════════════════════╝

Searching for: {query}
Location: {location}
Mode: {'Headless' if headless else 'Visual (browsers will open)'}

This will:
1. Research event info via Google
2. Search 4 ticket sites IN PARALLEL (watch the browsers!)
3. Analyze venue seating quality
4. Calculate VALUE scores for each ticket
5. Rank and present best options

Press Ctrl+C to cancel at any time.
""")

    # Run the search
    result = await run_ticket_search(
        query=query,
        location=location,
        headless=headless,
        sites=sites,
    )

    # Display results
    print_results(result)

    # Export to JSON for frontend
    export_json(result)

    return result


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nSearch cancelled by user.")
    except Exception as err:
        print(f"\nError: {err}")
        print("\nTroubleshooting:")
        print("  1. Check .env has GEMINI_API_KEY set")
        print("  2. Run: pip install -r requirements.txt")
        print("  3. Make sure you have Chrome installed")
        print("\nDocs: https://docs.stagehand.dev")
        sys.exit(1)

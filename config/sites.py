"""
Site configurations for ticket search agents.
Each site has specific instructions and URLs.
"""

SITE_CONFIGS = {
    "ticketmaster": {
        "url": "https://www.ticketmaster.com",
        "name": "Ticketmaster",
        "instructions": """You are searching Ticketmaster for tickets.

IMPORTANT:
- Include ALL fees in the price (service fee, facility fee)
- Click "See Price Details" or hover to get the true total price
- Note if tickets are "Official Platinum" (dynamic pricing)
- Extract section, row, and seat numbers when available
- If you see a price range, report the lower price
- Watch for "Verified Resale" tickets""",
        "max_steps": 20,
        "priority": 1,
    },
    "stubhub": {
        "url": "https://www.stubhub.com",
        "name": "StubHub",
        "instructions": """You are searching StubHub for tickets.

IMPORTANT:
- Click on listings to see the final "You Pay" price with all fees
- Note the seller rating if visible
- StubHub shows final price - use that number
- Check if tickets are instant download or will be transferred
- Look for the "Best Value" or "Great Deal" badges""",
        "max_steps": 20,
        "priority": 2,
    },
    "seatgeek": {
        "url": "https://www.seatgeek.com",
        "name": "SeatGeek",
        "instructions": """You are searching SeatGeek for tickets.

IMPORTANT:
- SeatGeek shows a "Deal Score" (good, great, etc.) - note this
- Prices shown usually include fees
- Look for the green "Good Deal" indicators
- Extract the section and row information
- Note if it says "Instant Download" """,
        "max_steps": 20,
        "priority": 3,
    },
    "tickpick": {
        "url": "https://www.tickpick.com",
        "name": "TickPick",
        "instructions": """You are searching TickPick for tickets.

IMPORTANT:
- TickPick has NO FEES - the price shown is what you pay
- This often makes them the cheapest option
- Look for their "BestPick" recommendations
- Extract section, row, and quantity available""",
        "max_steps": 20,
        "priority": 4,
    },
    "vividseats": {
        "url": "https://www.vividseats.com",
        "name": "VividSeats",
        "instructions": """You are searching VividSeats for tickets.

IMPORTANT:
- Check the final price including fees at checkout preview
- Note their "Super Seller" verified sellers
- Look for promo codes that might be displayed
- Extract section, row, and seat numbers""",
        "max_steps": 20,
        "priority": 5,
    },
}


def get_site_config(site_name: str) -> dict:
    """Get configuration for a specific site."""
    if site_name not in SITE_CONFIGS:
        raise ValueError(f"Unknown site: {site_name}. Valid: {list(SITE_CONFIGS.keys())}")
    return SITE_CONFIGS[site_name]


def get_all_sites() -> list[str]:
    """Get list of all configured sites, ordered by priority."""
    return sorted(SITE_CONFIGS.keys(), key=lambda s: SITE_CONFIGS[s]["priority"])

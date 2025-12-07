"""
Site Search Agents: Specialized agents for each ticketing platform.
Each agent searches its assigned site and extracts ticket listings.
"""

import re
import uuid
from typing import Optional

from .base import BaseAgent
from models import EventInfo, TicketListing, SiteSearchResult, AgentStatus


# Site configurations
SITE_CONFIGS = {
    "ticketmaster": {
        "url": "https://www.ticketmaster.com",
        "name": "Ticketmaster",
        "instructions": """You are searching Ticketmaster for tickets.

IMPORTANT:
- Include ALL fees in the price (service fee, facility fee)
- Click "See Price Details" or hover to get the true total price
- Note if tickets are "Official Platinum" (dynamic pricing - often overpriced)
- Extract section, row, and seat numbers when available
- If you see a price range, report the lower price
- Watch for "Verified Resale" tickets - note this in your findings""",
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
    },
    "tickpick": {
        "url": "https://www.tickpick.com",
        "name": "TickPick",
        "instructions": """You are searching TickPick for tickets.

IMPORTANT:
- TickPick has NO FEES - the price shown is what you pay
- This often makes them the cheapest option
- Look for their "BestPick" recommendations
- Extract section, row, and quantity available
- Note any special deals or promotions""",
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
    },
}


class SiteSearchAgent(BaseAgent):
    """Agent that searches a specific ticketing site for listings."""

    def __init__(
        self,
        site_name: str,
        headless: bool = False,
    ):
        if site_name not in SITE_CONFIGS:
            raise ValueError(f"Unknown site: {site_name}. Valid: {list(SITE_CONFIGS.keys())}")

        self.site_name = site_name
        self.site_config = SITE_CONFIGS[site_name]

        super().__init__(
            name=f"{self.site_config['name']}Agent",
            max_steps=30,  # Increased for thorough price extraction
            headless=headless,
        )

    def get_system_instructions(self) -> str:
        return f"""You are a ticket search specialist for {self.site_config['name']}.

{self.site_config['instructions']}

EXTRACTION FORMAT:
For each ticket listing you find, extract:
- Section name
- Row (if available)
- Number of tickets available
- Price per ticket
- Total price with fees
- Any special notes

CRITICAL: When viewing ticket listings:
- NEVER use scroll_at action - it causes validation errors
- Use scroll_document or keypress PageDown to see more tickets
- Extract visible tickets BEFORE scrolling
- Format your findings clearly: "Section: X, Row: Y, Price: $Z"

Be thorough - review all available listings to find the best options.
If you encounter a CAPTCHA or are blocked, report this and try to proceed if possible."""

    async def run(self, event_info: EventInfo) -> SiteSearchResult:
        """
        Search the site for ticket listings.

        Args:
            event_info: Event details from ResearchAgent

        Returns:
            SiteSearchResult with all found listings
        """
        result = SiteSearchResult(
            site_name=self.site_name,
            status=AgentStatus.PENDING,
        )

        try:
            async with self:
                # Navigate to the site
                await self.navigate(self.site_config["url"])

                # Build search instruction
                # Prioritize city over potentially mismatched venue names
                search_instruction = f"""Search for tickets to: {event_info.artist_name}

City: {event_info.city}

Steps:
1. Use the search bar to search for "{event_info.artist_name}"
2. Set location filter to "{event_info.city}" (ignore other cities)
3. Select ANY show in {event_info.city} - the exact venue doesn't matter
4. View the ticket listings page
5. Extract pricing for ALL visible tickets - note section, row, and price for each
6. Use scroll_document (NOT scroll_at) if you need to see more listings

CRITICAL INSTRUCTIONS:
- NEVER use scroll_at - it causes errors. Use scroll_document or keypress PageDown instead.
- Extract data from what's currently visible before scrolling
- List each ticket with: Section, Row (if shown), Price
- Example format: "Section: Upper Balc Center, Row: V, Price: $11"

IMPORTANT: Only find tickets in or very near {event_info.city}. If no shows exist there, report that clearly.

After viewing tickets, provide a detailed summary with specific sections and prices."""

                # Execute the search
                agent_result = await self.execute_agent(search_instruction)

                result.status = AgentStatus.SUCCESS if agent_result["success"] else AgentStatus.PARTIAL
                result.search_url = self.stagehand.page.url if self.stagehand else ""

                # Parse listings from agent output
                result.listings = self._parse_listings(agent_result)

        except Exception as e:
            result.status = AgentStatus.FAILED
            result.error_message = str(e)
            print(f"[{self.name}] Error: {e}")

        return result

    def _parse_listings(self, agent_result: dict) -> list[TicketListing]:
        """Parse agent output into TicketListing objects."""
        listings = []

        if not agent_result.get("success"):
            return listings

        # The agent returns a complex object - try multiple extraction methods
        result = agent_result.get("result")

        # Collect all text from the result object
        result_texts = []

        # Method 1: Try common text attributes
        for attr in ['message', 'text', 'content', 'output', 'reasoning', 'thoughts']:
            if hasattr(result, attr):
                text = getattr(result, attr)
                if text:
                    result_texts.append(str(text))

        # Method 2: If result is a dict, get all string values
        if isinstance(result, dict):
            for key, value in result.items():
                if isinstance(value, str) and len(value) > 10:
                    result_texts.append(value)

        # Method 3: Get string representation
        result_texts.append(str(result))

        # Method 4: Check for __dict__ attribute (object introspection)
        if hasattr(result, '__dict__'):
            for key, value in result.__dict__.items():
                if isinstance(value, str) and len(value) > 10:
                    result_texts.append(value)

        # Combine all text sources
        full_text = "\n".join(result_texts)

        print(f"[{self.name}] Parsing result (first 1000 chars): {full_text[:1000]}")

        # Enhanced parsing patterns
        # Pattern 1: "Section: X, Row: Y, Price: $Z"
        structured_pattern = r'Section:\s*([^,\n]+)(?:,\s*Row:\s*([^,\n]+))?,.*?Price:\s*\$(\d+(?:\.\d{2})?)'
        structured_matches = re.findall(structured_pattern, full_text, re.IGNORECASE)

        for section, row, price in structured_matches:
            listing = TicketListing(
                source=self.site_name,
                section=section.strip(),
                row=row.strip() if row else "",
                price_per_ticket=float(price),
                total_price=float(price),
                quantity=2,
            )
            listings.append(listing)

        # Pattern 2: Fallback to simple price extraction if structured parsing fails
        if not listings:
            price_pattern = r'\$(\d+(?:\.\d{2})?)'
            prices = re.findall(price_pattern, full_text)

            # Look for section patterns (more flexible)
            section_patterns = [
                r'Section:\s*([A-Za-z0-9\s]+?)(?:,|\n|Row)',
                r'(?:Section|Sec\.?)\s*([A-Za-z0-9\s]+)',
                r'([A-Z][a-z]+\s+Balc(?:ony)?\s+(?:Center|Left|Right|Centre))',
                r'([A-Z][a-z]+\s+(?:Floor|Orchestra|Mezzanine|Balcony))',
            ]

            sections = []
            for pattern in section_patterns:
                sections = re.findall(pattern, full_text, re.IGNORECASE)
                if sections:
                    break

            # Look for row patterns
            row_pattern = r'Row:\s*([A-Za-z0-9]+)'
            rows = re.findall(row_pattern, full_text, re.IGNORECASE)

            print(f"[{self.name}] Found {len(prices)} prices, {len(sections)} sections, {len(rows)} rows")

            # Create listings from found data
            for i, price in enumerate(prices[:10]):  # Limit to 10 listings
                section = sections[i].strip() if i < len(sections) else f"Section {i+1}"
                row = rows[i].strip() if i < len(rows) else ""

                listing = TicketListing(
                    source=self.site_name,
                    section=section,
                    row=row,
                    price_per_ticket=float(price),
                    total_price=float(price),  # Agent should report with fees
                    quantity=2,  # Default assumption
                )
                listings.append(listing)

        # If still no prices found, create a placeholder
        if not listings:
            print(f"[{self.name}] WARNING: Could not extract any pricing data")
            print(f"[{self.name}] Full result object type: {type(result)}")
            print(f"[{self.name}] Result attributes: {dir(result) if hasattr(result, '__dir__') else 'N/A'}")
            listings.append(TicketListing(
                source=self.site_name,
                section="Various",
                notes="Could not extract specific pricing - check site directly",
            ))

        # Deduplicate listings (agent reasoning can repeat the same data)
        seen = set()
        unique_listings = []
        for listing in listings:
            # Create a unique key based on section, row, and price
            key = (listing.section, listing.row or "", listing.price_per_ticket)
            if key not in seen:
                seen.add(key)
                unique_listings.append(listing)

        if len(listings) != len(unique_listings):
            print(f"[{self.name}] Deduplicated {len(listings)} listings down to {len(unique_listings)} unique")

        return unique_listings


def create_site_agent(site_name: str, headless: bool = False) -> SiteSearchAgent:
    """Factory function to create a site-specific search agent."""
    return SiteSearchAgent(site_name=site_name, headless=headless)


async def run_site_search(site_name: str, event_info: EventInfo, headless: bool = False) -> SiteSearchResult:
    """Convenience function to run a site search."""
    agent = create_site_agent(site_name, headless=headless)
    return await agent.run(event_info)

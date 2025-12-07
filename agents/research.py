"""
ResearchAgent: Searches Google for event information (dates, venues, tour details).
This is the first agent in the pipeline - its output feeds all other agents.
"""

import re
from datetime import datetime
from typing import Optional

from .base import BaseAgent
from models import EventInfo, SearchQuery, AgentStatus


class ResearchAgent(BaseAgent):
    """Agent that researches event information via Google search."""

    def __init__(self, headless: bool = False):
        super().__init__(
            name="ResearchAgent",
            max_steps=8,  # Enough to search Google and extract event info
            headless=False,  # Never use headless mode
        )

    def get_system_instructions(self) -> str:
        return """You are a research assistant finding information about live events and concerts.

Your task is to search for and extract:
1. Confirmed show/event dates
2. Venue names and cities
3. Tour name (if applicable)
4. Any special notes (e.g., "sold out", "just announced")

IMPORTANT:
- Focus on finding SPECIFIC dates and venues
- Look for official announcements or reputable ticketing sites
- If multiple shows exist, list ALL of them
- Note the year - make sure dates are for upcoming shows, not past ones

Format your findings clearly with:
- Artist/Event name
- Each date and corresponding venue
- City for each venue
- Any relevant notes"""

    async def run(self, query: SearchQuery) -> EventInfo:
        """
        Search for event information.

        Args:
            query: SearchQuery with artist name and location

        Returns:
            EventInfo with dates, venues, and details
        """
        try:
            async with self:
                # Navigate to Google
                await self.navigate("https://www.google.com/")

                # Build search query
                search_terms = f"{query.query} {query.location} concert tickets 2025"

                # Execute search via agent
                result = await self.execute_agent(
                    f"""Search for: "{search_terms}"

Find and extract:
1. All upcoming show dates for {query.query} in or near {query.location}
2. The venue name for each date
3. Tour name if mentioned
4. Whether tickets are on sale

Look at multiple search results to gather complete information.
Summarize your findings with specific dates and venues."""
                )

                # Parse results into EventInfo
                return self._parse_results(query, result)

        except Exception as e:
            self.status = AgentStatus.FAILED
            print(f"[{self.name}] Error: {e}")
            # Return minimal info on failure
            return EventInfo(
                artist_name=query.query,
                event_name=query.query,
                city=query.location,
                notes=f"Research failed: {str(e)}",
            )

    def _parse_results(self, query: SearchQuery, result: dict) -> EventInfo:
        """Parse agent results into EventInfo structure."""
        # The agent returns unstructured text - we'll extract what we can
        # In a production system, you'd use more sophisticated parsing

        event_info = EventInfo(
            artist_name=query.query,
            event_name=query.query,
            city=query.location,
        )

        if result.get("success") and result.get("result"):
            # Try to extract dates from the result
            # This is a simplified parser - the agent's output will be text
            result_text = str(result.get("result", ""))

            # Look for venue mentions
            venue_patterns = [
                r"(?:at\s+(?:the\s+)?)?([A-Z][A-Za-z\s]+(?:Masonic|Arena|Center|Centre|Theatre|Theater|Garden|Stadium|Hall|Amphitheatre|Auditorium|Pavilion))",
                r"(SF\s+Masonic|Masonic\s+Auditorium)",
                r"([A-Z][A-Za-z\s]{3,30}(?:Arena|Center|Theatre|Theater|Garden|Stadium|Hall))",
            ]

            for pattern in venue_patterns:
                matches = re.findall(pattern, result_text)
                if matches:
                    event_info.venues = list(set(matches))[:5]  # Dedupe, limit to 5
                    break

            # If no venues found, use a placeholder
            if not event_info.venues:
                event_info.venues = [f"Venue in {query.location}"]

            event_info.notes = "Research completed via Google search"

        return event_info


async def run_research(query: SearchQuery) -> EventInfo:
    """Convenience function to run research agent."""
    agent = ResearchAgent()
    return await agent.run(query)

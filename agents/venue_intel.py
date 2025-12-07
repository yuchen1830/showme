"""
VenueIntelAgent: Gathers intelligence about venues - seating charts, reviews, best sections.
This helps the ValueAnalyzerAgent determine seat quality scores.
"""

import re
from typing import Optional

from .base import BaseAgent
from models import VenueIntel, SectionQuality, AgentStatus


class VenueIntelAgent(BaseAgent):
    """Agent that researches venue seating quality and recommendations."""

    def __init__(self, headless: bool = False):
        super().__init__(
            name="VenueIntelAgent",
            max_steps=15,
            headless=headless,
        )

    def get_system_instructions(self) -> str:
        return """You are a venue research specialist helping people find the best seats.

Your task is to gather intelligence about a specific venue:

1. SEATING CHART
   - Find and examine the venue's seating chart
   - Identify all major sections (Floor, Lower, Upper, Balcony, etc.)

2. SECTION QUALITY
   - Research which sections have the best views
   - Find reviews mentioning specific sections
   - Note any "obstructed view" warnings

3. VALUE RECOMMENDATIONS
   - Identify sections that offer good views at lower prices
   - Note premium sections and whether they're worth it
   - Find any "insider tips" about the venue

4. SECTIONS TO AVOID
   - Identify sections with known issues (pillars, bad angles)
   - Note any reviews warning about specific areas

Format your findings as a clear assessment of each section's quality (rate 1-10) and value."""

    async def run(self, venue_name: str, city: str) -> VenueIntel:
        """
        Research a venue for seating quality information.

        Args:
            venue_name: Name of the venue
            city: City where venue is located

        Returns:
            VenueIntel with section ratings and recommendations
        """
        result = VenueIntel(
            venue_name=venue_name,
            city=city,
        )

        try:
            async with self:
                # Navigate to Google
                await self.navigate("https://www.google.com/")

                # Search for venue seating information
                search_instruction = f"""Research the seating at {venue_name} in {city}.

Step 1: Search for "{venue_name} seating chart"
- Find and examine the seating chart image
- Note all section names

Step 2: Search for "{venue_name} best seats reddit" or "{venue_name} seat review"
- Find recommendations from people who've been there
- Note which sections get positive reviews

Step 3: Search for "{venue_name} worst seats" or "{venue_name} obstructed view"
- Find warnings about sections to avoid

Summarize your findings:
- List each major section with a quality rating (1-10)
- Identify 2-3 "best value" sections (good quality, reasonable price)
- Identify any sections to avoid
- Include any insider tips you find"""

                agent_result = await self.execute_agent(search_instruction)

                # Parse results
                result = self._parse_results(agent_result, venue_name, city)

        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            # Return default ratings on failure
            result.notes = f"Research failed: {str(e)}"
            result.sections = self._get_default_sections()

        return result

    def _parse_results(self, agent_result: dict, venue_name: str, city: str) -> VenueIntel:
        """Parse agent results into VenueIntel structure."""
        intel = VenueIntel(
            venue_name=venue_name,
            city=city,
        )

        result_text = str(agent_result.get("result", ""))

        # Try to extract section ratings from text
        # Look for patterns like "Section 100: 8/10" or "Floor - 9"
        section_patterns = [
            r'(Floor|Orchestra|Pit|VIP|Section\s*\d+|Lower|Upper|Balcony|Mezzanine|Club|Premium)[\s:]+(\d+)(?:/10)?',
            r'(Floor|Orchestra|Pit|VIP|Lower|Upper|Balcony|Mezzanine|Club|Premium)[^\d]*(\d+)\s*(?:out of|/)\s*10',
        ]

        found_sections = set()
        for pattern in section_patterns:
            matches = re.findall(pattern, result_text, re.IGNORECASE)
            for section_name, score in matches:
                if section_name.lower() not in found_sections:
                    found_sections.add(section_name.lower())
                    intel.sections.append(SectionQuality(
                        section_name=section_name,
                        quality_score=min(10, max(1, float(score))),
                    ))

        # If no sections found, use defaults
        if not intel.sections:
            intel.sections = self._get_default_sections()

        # Look for "best" or "recommended" sections
        best_patterns = [
            r'(?:best|recommend|great)[^.]*(?:section|seats?)[^.]*(\w+)',
            r'(\w+)\s+(?:section|seats?)[^.]*(?:best|great|excellent)',
        ]
        for pattern in best_patterns:
            matches = re.findall(pattern, result_text, re.IGNORECASE)
            intel.best_value_sections.extend([m for m in matches if len(m) > 2])

        # Look for sections to avoid
        avoid_patterns = [
            r'(?:avoid|bad|terrible|worst)[^.]*(?:section|seats?)[^.]*(\w+)',
            r'(\w+)\s+(?:section|seats?)[^.]*(?:avoid|bad|obstructed)',
        ]
        for pattern in avoid_patterns:
            matches = re.findall(pattern, result_text, re.IGNORECASE)
            intel.avoid_sections.extend([m for m in matches if len(m) > 2])

        intel.tips = [
            f"Research completed for {venue_name}",
            "Quality scores based on online reviews and recommendations",
        ]

        return intel

    def _get_default_sections(self) -> list[SectionQuality]:
        """Return default section quality ratings when research fails."""
        return [
            SectionQuality(section_name="Floor", quality_score=9.0, notes="Usually best view"),
            SectionQuality(section_name="Orchestra", quality_score=8.5, notes="Great sightlines"),
            SectionQuality(section_name="Lower", quality_score=7.5, notes="Good value"),
            SectionQuality(section_name="Club", quality_score=7.0, notes="Premium amenities"),
            SectionQuality(section_name="Mezzanine", quality_score=6.5, notes="Elevated view"),
            SectionQuality(section_name="Upper", quality_score=5.0, notes="Budget option"),
            SectionQuality(section_name="Balcony", quality_score=4.5, notes="Distant but cheap"),
        ]


async def run_venue_intel(venue_name: str, city: str) -> VenueIntel:
    """Convenience function to run venue intel agent."""
    agent = VenueIntelAgent()
    return await agent.run(venue_name, city)

"""
Ticket Search Orchestrator: Coordinates multiple agents for comprehensive ticket search.
Implements hybrid architecture: parallel site searches with sequential analysis.
"""

import asyncio
from datetime import datetime
from typing import Optional

from models import (
    SearchQuery,
    EventInfo,
    VenueIntel,
    SiteSearchResult,
    OrchestratorResult,
    AgentStatus,
)
from agents import ResearchAgent, SiteSearchAgent, VenueIntelAgent, ValueAnalyzerAgent


# Sites to search in parallel
DEFAULT_SITES = ["ticketmaster", "stubhub", "seatgeek", "tickpick"]

# Timeout for each site search (5 minutes - agents need time to extract pricing)
SITE_TIMEOUT = 500.0

# Maximum concurrent browser sessions
MAX_CONCURRENT = 4


class TicketSearchOrchestrator:
    """
    Orchestrates multi-agent ticket search.

    Flow:
    1. ResearchAgent → Find event info (sequential)
    2. SiteSearchAgents + VenueIntelAgent → Search sites & gather venue intel (parallel)
    3. ValueAnalyzerAgent → Score and rank results (sequential)
    """

    def __init__(
        self,
        sites: Optional[list[str]] = None,
        headless: bool = False,
    ):
        self.sites = sites or DEFAULT_SITES
        self.headless = headless
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    async def search(self, query: str, location: str = "") -> OrchestratorResult:
        """
        Execute a full ticket search.

        Args:
            query: Artist or event name
            location: City or location

        Returns:
            OrchestratorResult with all findings
        """
        search_query = SearchQuery(query=query, location=location)
        result = OrchestratorResult(
            query=search_query,
            started_at=datetime.now(),
        )

        print(f"\n{'='*60}")
        print(f"TICKET SEARCH: {query}")
        print(f"Location: {location}")
        print(f"Sites: {', '.join(self.sites)}")
        print(f"{'='*60}\n")

        try:
            # PHASE 1: Research (Sequential)
            print("[PHASE 1] Researching event information...")
            result.event_info = await self._run_research(search_query)
            print(f"  Found: {result.event_info.event_name}")
            print(f"  Venues: {', '.join(result.event_info.venues)}")

            # PHASE 2: Parallel Search + Venue Intel
            print("\n[PHASE 2] Searching sites in parallel...")
            result.search_results, result.venue_intel = await self._run_parallel_phase(
                result.event_info
            )

            # Report search results
            for site_name, site_result in result.search_results.items():
                status = "✓" if site_result.status == AgentStatus.SUCCESS else "✗"
                count = len(site_result.listings)
                print(f"  {status} {site_name}: {count} listings")

            # PHASE 3: Analysis (Sequential)
            print("\n[PHASE 3] Analyzing value scores...")
            analyzer = ValueAnalyzerAgent()
            result.ranked_seats, result.events = analyzer.analyze(
                result.search_results,
                result.venue_intel,
                result.event_info,
            )
            print(f"  Analyzed {len(result.ranked_seats)} seats")

        except Exception as e:
            result.errors.append(f"Orchestration error: {str(e)}")
            print(f"\n[ERROR] {e}")

        result.completed_at = datetime.now()
        duration = (result.completed_at - result.started_at).total_seconds()
        print(f"\n{'='*60}")
        print(f"Search completed in {duration:.1f}s")
        print(f"{'='*60}\n")

        return result

    async def _run_research(self, query: SearchQuery) -> EventInfo:
        """Run the research agent to gather event info."""
        agent = ResearchAgent(headless=self.headless)
        return await agent.run(query)

    async def _run_parallel_phase(
        self, event_info: EventInfo
    ) -> tuple[dict[str, SiteSearchResult], VenueIntel]:
        """
        Run site searches and venue intel in parallel.

        Uses asyncio.TaskGroup for clean exception handling.
        Each site gets its own browser session.
        """
        search_results = {}
        venue_intel = None

        async def search_site(site_name: str) -> tuple[str, SiteSearchResult]:
            """Search a single site with timeout."""
            async with self.semaphore:
                try:
                    result = await asyncio.wait_for(
                        self._run_site_search(site_name, event_info),
                        timeout=SITE_TIMEOUT,
                    )
                    return site_name, result
                except asyncio.TimeoutError:
                    return site_name, SiteSearchResult(
                        site_name=site_name,
                        status=AgentStatus.FAILED,
                        error_message="Search timed out",
                    )
                except Exception as e:
                    return site_name, SiteSearchResult(
                        site_name=site_name,
                        status=AgentStatus.FAILED,
                        error_message=str(e),
                    )

        async def get_venue_intel() -> VenueIntel:
            """Get venue intelligence."""
            async with self.semaphore:
                venue_name = event_info.venues[0] if event_info.venues else "Unknown Venue"
                agent = VenueIntelAgent(headless=self.headless)
                return await agent.run(venue_name, event_info.city)

        # Run all tasks in parallel
        tasks = []

        # Site search tasks
        for site_name in self.sites:
            tasks.append(asyncio.create_task(search_site(site_name)))

        # Venue intel task
        venue_task = asyncio.create_task(get_venue_intel())

        # Wait for all site searches
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for result in results:
            if isinstance(result, tuple):
                site_name, site_result = result
                search_results[site_name] = site_result
            elif isinstance(result, Exception):
                print(f"  [ERROR] Task failed: {result}")

        # Wait for venue intel
        try:
            venue_intel = await venue_task
        except Exception as e:
            print(f"  [ERROR] Venue intel failed: {e}")
            venue_intel = VenueIntel(
                venue_name="Unknown",
                city=event_info.city,
            )

        return search_results, venue_intel

    async def _run_site_search(
        self, site_name: str, event_info: EventInfo
    ) -> SiteSearchResult:
        """Run a single site search agent."""
        agent = SiteSearchAgent(site_name=site_name, headless=self.headless)
        return await agent.run(event_info)


async def run_ticket_search(
    query: str,
    location: str = "",
    sites: Optional[list[str]] = None,
    headless: bool = False,
) -> OrchestratorResult:
    """
    Convenience function to run a ticket search.

    Args:
        query: Artist or event name
        location: City or location
        sites: List of sites to search (default: all)
        headless: Run browsers without UI (default: False)

    Returns:
        OrchestratorResult with all findings
    """
    orchestrator = TicketSearchOrchestrator(sites=sites, headless=headless)
    return await orchestrator.search(query, location)

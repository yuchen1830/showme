"""
FastAPI dependencies
"""
from functools import lru_cache
import os

from src.application.use_cases.search_use_case import SearchUseCase
from src.infrastructure.api.agent_orchestrator_client import AgentOrchestratorClient


@lru_cache()
def get_settings():
    """Get application settings"""
    return {
        "use_agents": os.getenv("USE_AGENTS", "true").lower() == "true",
    }


def get_search_use_case() -> SearchUseCase:
    """Dependency for search use case - uses AI agent orchestrator"""
    return SearchUseCase(
        agent_client=AgentOrchestratorClient()
    )


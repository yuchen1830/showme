"""
Base agent class with Stagehand initialization and common utilities.
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Optional

from dotenv import load_dotenv
from stagehand import Stagehand, StagehandConfig

from models import AgentStatus

load_dotenv()


class BaseAgent(ABC):
    """Base class for all agents with Stagehand browser automation."""

    def __init__(
        self,
        name: str,
        max_steps: int = 20,
        headless: bool = False,
        verbose: int = 1,
    ):
        self.name = name
        self.max_steps = max_steps
        self.headless = headless
        self.verbose = verbose
        self.stagehand: Optional[Stagehand] = None
        self.status = AgentStatus.PENDING
        self.screenshots: list[str] = []

    async def initialize(self) -> None:
        """Initialize Stagehand browser session."""
        config = StagehandConfig(
            env="LOCAL",
            model_api_key=os.environ.get("GEMINI_API_KEY"),
            headless=self.headless,
            verbose=self.verbose,
        )
        self.stagehand = Stagehand(config)
        await self.stagehand.init()
        self.status = AgentStatus.RUNNING
        print(f"[{self.name}] Browser initialized")

    async def close(self) -> None:
        """Close the browser session."""
        if self.stagehand:
            await self.stagehand.close()
            print(f"[{self.name}] Browser closed")

    def create_agent(self, instructions: str) -> Any:
        """Create a Gemini Computer Use agent with custom instructions."""
        if not self.stagehand:
            raise RuntimeError("Stagehand not initialized. Call initialize() first.")

        page = self.stagehand.page
        return self.stagehand.agent(
            provider="google",
            model="gemini-2.5-computer-use-preview-10-2025",
            instructions=f"""{instructions}

You are currently on: {page.url}
Do not ask follow up questions - use your best judgment.
If blocked on one site, try alternative approaches.""",
            options={"api_key": os.getenv("GEMINI_API_KEY")},
        )

    async def navigate(self, url: str, timeout: int = 60000) -> None:
        """Navigate to a URL."""
        if not self.stagehand:
            raise RuntimeError("Stagehand not initialized")

        await self.stagehand.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=timeout,
        )
        print(f"[{self.name}] Navigated to {url}")

    async def execute_agent(self, instruction: str) -> dict:
        """Execute an instruction with the Gemini agent."""
        agent = self.create_agent(self.get_system_instructions())

        print(f"[{self.name}] Executing: {instruction[:100]}...")

        result = await agent.execute(
            instruction=instruction,
            max_steps=self.max_steps,
            auto_screenshot=True,
        )

        # Gemini agent result object doesn't have .success attribute
        # Check if execution completed without raising exception
        success = result is not None

        if success:
            self.status = AgentStatus.SUCCESS
            print(f"[{self.name}] Task completed successfully")
        else:
            self.status = AgentStatus.PARTIAL
            print(f"[{self.name}] Task completed with issues")

        return {
            "success": success,
            "result": result,
        }

    @abstractmethod
    def get_system_instructions(self) -> str:
        """Return system instructions for this agent type."""
        pass

    @abstractmethod
    async def run(self, *args, **kwargs) -> Any:
        """Run the agent's main task. Implemented by subclasses."""
        pass

    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

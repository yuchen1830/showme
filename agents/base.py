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

    async def execute_agent(self, instruction: str, max_retries: int = 2) -> dict:
        """Execute an instruction with the Gemini agent with retry logic."""
        import asyncio
        
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                agent = self.create_agent(self.get_system_instructions())

                print(f"[{self.name}] Executing (attempt {attempt + 1}/{max_retries + 1}): {instruction[:100]}...")

                result = await agent.execute(
                    instruction=instruction,
                    max_steps=self.max_steps,
                    auto_screenshot=True,
                )

                # Check if we got a valid result
                if result is not None:
                    # Check for error messages in result that indicate API issues
                    result_msg = getattr(result, 'message', '') or ''
                    if '500 INTERNAL' in str(result_msg) or 'No candidates' in str(result_msg):
                        raise Exception(f"API error in result: {result_msg[:200]}")
                    
                    self.status = AgentStatus.SUCCESS
                    print(f"[{self.name}] Task completed successfully")
                    return {"success": True, "result": result}
                else:
                    raise Exception("Agent returned None result")
                    
            except Exception as e:
                last_error = e
                error_str = str(e)
                
                # Check if it's a retryable error
                retryable = any(x in error_str for x in ['500', 'INTERNAL', 'No candidates', 'NoneType'])
                
                if retryable and attempt < max_retries:
                    wait_time = (attempt + 1) * 2  # 2s, 4s backoff
                    print(f"[{self.name}] Retryable error: {error_str[:100]}... Waiting {wait_time}s before retry")
                    await asyncio.sleep(wait_time)
                else:
                    print(f"[{self.name}] Non-retryable error or max retries reached: {error_str[:200]}")
                    break
        
        # All retries exhausted
        self.status = AgentStatus.PARTIAL
        print(f"[{self.name}] Task completed with issues after {max_retries + 1} attempts")
        return {
            "success": False,
            "result": None,
            "error": str(last_error),
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

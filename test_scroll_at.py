"""
Test script to verify scroll_at action works with Gemini CUA
"""
import asyncio
import os
from stagehand import Stagehand
from dotenv import load_dotenv

load_dotenv()


async def test_scroll_at():
    """Test if scroll_at action works."""
    print("Testing scroll_at action...")
    
    stagehand = Stagehand(
        model_name="gemini/gemini-2.5-flash-preview-04-17",
        headless=False,
        env="LOCAL",
    )
    
    try:
        await stagehand.init()
        
        # Navigate to TickPick event page with scrollable ticket list
        await stagehand.page.goto("https://www.tickpick.com/buy-louis-c-k-tickets-stockton-ca-12-14-25-7pm/6653612/")
        await asyncio.sleep(3)
        
        # Create the agent
        agent = stagehand.agent(
            provider="google",
            model="gemini-2.5-computer-use-preview-10-2025",
            options={"api_key": os.getenv("GEMINI_API_KEY")},
            instructions="""You are testing the scroll_at action.
You MUST use scroll_at to scroll the ticket list panel.""",
        )
        
        # Execute with explicit scroll_at instruction
        result = await agent.execute(
            instruction="""
IMPORTANT: You MUST use the scroll_at action!

The ticket list is on the LEFT side of the page (x ~250 to 400).

STEPS:
1. First, read the first 2-3 visible ticket listings (Section, Row, Price)
2. THEN use scroll_at with these parameters:
   - x: 300 (left side where ticket list is)
   - y: 700 (middle of ticket list area)
   - direction: "down"
   - magnitude: 400
3. After scrolling, read the new ticket listings

Output format:
BEFORE SCROLL:
- Section: [name], Row: [row], Price: $[amount]

AFTER SCROLL:
- Section: [name], Row: [row], Price: $[amount]
""",
            max_steps=10,
        )
        
        print("\n" + "="*60)
        print("RESULT:")
        print("="*60)
        print(f"Success: {result.completed}")
        print(f"Message: {result.message[:1000] if result.message else 'No message'}")
        
        # Check if scroll_at was used
        if result.actions:
            print("\nActions taken:")
            for action in result.actions:
                action_str = str(action)
                print(f"  - {action_str[:100]}")
                if "scroll" in action_str.lower():
                    print("    *** SCROLL ACTION FOUND! ***")
        
    finally:
        await stagehand.close()


if __name__ == "__main__":
    asyncio.run(test_scroll_at())

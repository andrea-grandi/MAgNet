#!/usr/bin/env python3
"""Quick check to verify all A2A agents are running."""

import asyncio
import sys
import httpx
from a2a.client.card_resolver import A2ACardResolver

AGENTS = {
    "Supervisor": "http://localhost:8001",
    "Calculator": "http://localhost:8002",
    "Coder": "http://localhost:8003",
    "Translator": "http://localhost:8004"
}

async def check_agent(name: str, url: str) -> bool:
    """Check if an agent is responding."""
    try:
        print(f"Checking {name} at {url}...", end=" ")
        async with httpx.AsyncClient() as client:
            resolver = A2ACardResolver(httpx_client=client, base_url=url)
            card = await resolver.get_agent_card()
            print(f"✓ OK - {card.name}")
            return True
    except Exception as e:
        print(f"✗ FAILED - {str(e)}")
        return False

async def main():
    """Check all agents."""
    print("="*60)
    print("Checking A2A Agents")
    print("="*60)
    
    results = []
    for name, url in AGENTS.items():
        result = await check_agent(name, url)
        results.append(result)
    
    print("="*60)
    success = sum(results)
    total = len(results)
    print(f"Result: {success}/{total} agents responding")
    print("="*60)
    
    if success < total:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

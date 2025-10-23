"""
Test script for the A2A Supervisor Multi-Agent Architecture.

This script tests the communication between:
1. Supervisor Agent (orchestrator)
2. Calculator Agent (math operations via MCP)
3. Coder Agent (programming tasks via MCP)
4. Translator Agent (translation tasks via MCP)

All agents communicate via the A2A (Agent-to-Agent) protocol.
"""

import asyncio
import logging
import httpx
from typing import Dict, Any
from a2a.client import ClientFactory, ClientConfig
from a2a.client.card_resolver import A2ACardResolver
from a2a.types import TextPart, Message, Role

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Agent URLs
SUPERVISOR_URL = "http://0.0.0.0:8001"
CALCULATOR_URL = "http://0.0.0.0:8002"
CODER_URL = "http://0.0.0.0:8003"
TRANSLATOR_URL = "http://0.0.0.0:8004"


class TestResults:
    """Store test results."""
    
    def __init__(self):
        self.tests: Dict[str, Dict[str, Any]] = {}
    
    def add_result(self, test_name: str, success: bool, response: str = "", error: str = ""):
        """Add a test result."""
        self.tests[test_name] = {
            "success": success,
            "response": response,
            "error": error
        }
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        
        passed = sum(1 for t in self.tests.values() if t["success"])
        total = len(self.tests)
        
        for test_name, result in self.tests.items():
            status = "✓ PASS" if result["success"] else "✗ FAIL"
            print(f"\n{status} - {test_name}")
            if result["success"]:
                print(f"  Response: {result['response'][:100]}...")
            else:
                print(f"  Error: {result['error']}")
        
        print("\n" + "="*80)
        print(f"Results: {passed}/{total} tests passed")
        print("="*80 + "\n")


async def send_a2a_message(agent_url: str, content: str, agent_name: str) -> str:
    """Send a message to an agent via A2A protocol.
    
    Args:
        agent_url: The agent's A2A endpoint URL
        content: Message content to send
        agent_name: Name of the agent for logging
        
    Returns:
        The agent's response
    """
    logger.info(f"Sending message to {agent_name} at {agent_url}")
    logger.debug(f"Message: {content}")
    
    # Get agent card and create client
    async with httpx.AsyncClient() as httpx_client:
        card_resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=agent_url
        )
        agent_card = await card_resolver.get_agent_card()
        
        config = ClientConfig(
            streaming=True,
            httpx_client=httpx_client
        )
        factory = ClientFactory(config=config)
        client = factory.create(card=agent_card)
        
        # Create message
        text_part = TextPart(text=content)
        message = Message(
            message_id="test_request",
            role=Role.user,
            parts=[text_part]
        )
        
        # Send request and collect response
        response_parts = []
        async for event in client.send_message(message):
            # Event can be a tuple (Task, Event) or a Message
            if isinstance(event, tuple):
                _, actual_event = event
                event = actual_event
            
            # Check if it's a Message with parts
            if hasattr(event, 'parts') and event.parts:
                for part in event.parts:
                    if isinstance(part, TextPart):
                        response_parts.append(part.text)
                    elif hasattr(part, 'text'):
                        response_parts.append(part.text)
        
        response = " ".join(response_parts)
        logger.info(f"Received response from {agent_name}: {len(response)} chars")
        
        return response


async def test_direct_calculator_agent(results: TestResults):
    """Test direct communication with calculator agent."""
    test_name = "Direct Calculator Agent - Math Operation"
    logger.info(f"\n{'='*60}\nRunning: {test_name}\n{'='*60}")
    
    try:
        response = await send_a2a_message(
            CALCULATOR_URL,
            "Calculate 15 + 27 * 3",
            "Calculator Agent"
        )
        
        logger.info(f"Calculator response: {response}")
        results.add_result(test_name, True, response)
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        results.add_result(test_name, False, error=str(e))


async def test_direct_coder_agent(results: TestResults):
    """Test direct communication with coder agent."""
    test_name = "Direct Coder Agent - Code Generation"
    logger.info(f"\n{'='*60}\nRunning: {test_name}\n{'='*60}")
    
    try:
        response = await send_a2a_message(
            CODER_URL,
            "Write a Python function to calculate factorial",
            "Coder Agent"
        )
        
        logger.info(f"Coder response: {response[:200]}...")
        results.add_result(test_name, True, response)
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        results.add_result(test_name, False, error=str(e))


async def test_direct_translator_agent(results: TestResults):
    """Test direct communication with translator agent."""
    test_name = "Direct Translator Agent - Translation"
    logger.info(f"\n{'='*60}\nRunning: {test_name}\n{'='*60}")
    
    try:
        response = await send_a2a_message(
            TRANSLATOR_URL,
            "Translate 'Hello, how are you?' to Italian",
            "Translator Agent"
        )
        
        logger.info(f"Translator response: {response}")
        results.add_result(test_name, True, response)
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        results.add_result(test_name, False, error=str(e))


async def test_supervisor_math_routing(results: TestResults):
    """Test supervisor routing to calculator agent."""
    test_name = "Supervisor Routing - Math Task"
    logger.info(f"\n{'='*60}\nRunning: {test_name}\n{'='*60}")
    
    try:
        response = await send_a2a_message(
            SUPERVISOR_URL,
            "What is 123 + 456?",
            "Supervisor Agent"
        )
        
        logger.info(f"Supervisor response (math): {response}")
        results.add_result(test_name, True, response)
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        results.add_result(test_name, False, error=str(e))


async def test_supervisor_coding_routing(results: TestResults):
    """Test supervisor routing to coder agent."""
    test_name = "Supervisor Routing - Coding Task"
    logger.info(f"\n{'='*60}\nRunning: {test_name}\n{'='*60}")
    
    try:
        response = await send_a2a_message(
            SUPERVISOR_URL,
            "Write a Python function to check if a number is prime",
            "Supervisor Agent"
        )
        
        logger.info(f"Supervisor response (coding): {response[:200]}...")
        results.add_result(test_name, True, response)
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        results.add_result(test_name, False, error=str(e))


async def test_supervisor_translation_routing(results: TestResults):
    """Test supervisor routing to translator agent."""
    test_name = "Supervisor Routing - Translation Task"
    logger.info(f"\n{'='*60}\nRunning: {test_name}\n{'='*60}")
    
    try:
        response = await send_a2a_message(
            SUPERVISOR_URL,
            "Translate 'Good morning' to Spanish",
            "Supervisor Agent"
        )
        
        logger.info(f"Supervisor response (translation): {response}")
        results.add_result(test_name, True, response)
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        results.add_result(test_name, False, error=str(e))


async def test_supervisor_statistical_task(results: TestResults):
    """Test supervisor with complex statistical task."""
    test_name = "Supervisor Routing - Statistical Calculation"
    logger.info(f"\n{'='*60}\nRunning: {test_name}\n{'='*60}")
    
    try:
        response = await send_a2a_message(
            SUPERVISOR_URL,
            "Calculate the average of these numbers: 10, 20, 30, 40, 50",
            "Supervisor Agent"
        )
        
        logger.info(f"Supervisor response (statistics): {response}")
        results.add_result(test_name, True, response)
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        results.add_result(test_name, False, error=str(e))


async def main():
    """Main test runner."""
    print("\n" + "="*80)
    print("A2A SUPERVISOR MULTI-AGENT ARCHITECTURE TEST")
    print("="*80)
    print("\nTesting Agent-to-Agent communication with:")
    print(f"  - Supervisor Agent: {SUPERVISOR_URL}")
    print(f"  - Calculator Agent: {CALCULATOR_URL}")
    print(f"  - Coder Agent: {CODER_URL}")
    print(f"  - Translator Agent: {TRANSLATOR_URL}")
    print("="*80 + "\n")
    
    results = TestResults()
    
    # Test direct agent communication first
    print("\n### PHASE 1: Testing Direct Agent Communication ###\n")
    await test_direct_calculator_agent(results)
    await asyncio.sleep(1)  # Brief pause between tests
    
    await test_direct_coder_agent(results)
    await asyncio.sleep(1)
    
    await test_direct_translator_agent(results)
    await asyncio.sleep(1)
    
    # Test supervisor routing
    print("\n### PHASE 2: Testing Supervisor Routing via A2A ###\n")
    await test_supervisor_math_routing(results)
    await asyncio.sleep(1)
    
    await test_supervisor_coding_routing(results)
    await asyncio.sleep(1)
    
    await test_supervisor_translation_routing(results)
    await asyncio.sleep(1)
    
    await test_supervisor_statistical_task(results)
    
    # Print summary
    results.print_summary()


if __name__ == "__main__":
    asyncio.run(main())

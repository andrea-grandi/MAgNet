import asyncio
import json
from typing import Dict, Any


async def test_a2a_connection():
    """Test A2A connection to supervisor agent."""
    import httpx
    
    url = "http://localhost:8001/.well-known/agent-card.json"
    
    print("Testing A2A connection...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                agent_card = response.json()
                print("Agent card retrieved successfully!")
                print(f"Name: {agent_card.get('name')}")
                print(f"Description: {agent_card.get('description')}")
                print(f"Skills: {len(agent_card.get('skills', []))}")
                for skill in agent_card.get('skills', []):
                    print(f"- {skill.get('name')}: {skill.get('description')}")
                return True
            else:
                print(f"Failed to get agent card: {response.status_code}")
                return False
    except Exception as e:
        print(f"Error: {e}")
        return False


async def test_mcp_servers():
    """Test MCP server health checks."""
    import httpx
    
    servers = {
        "Calculator MCP": "http://0.0.0.0:8990/mcp",
        "Coding MCP": "http://0.0.0.0:8991/mcp",
        "Translation MCP": "http://0.0.0.0:8992/mcp"
    }
    
    print("\nTesting MCP servers connectivity...")
    all_healthy = True
    
    async with httpx.AsyncClient() as client:
        for name, url in servers.items():
            try:
                # Try to access the MCP endpoint (should return method not allowed or similar)
                response = await client.get(url, timeout=5.0)
                # MCP endpoints typically return 405 for GET requests (expecting POST)
                # or 200 with some info, or 406 (Not Acceptable)
                if response.status_code in [200, 405, 406, 400]:
                    print(f"{name}: reachable")
                else:
                    print(f"{name}: unexpected status {response.status_code}")
                    all_healthy = False
            except httpx.ConnectError:
                print(f"{name}: connection refused - server not running")
                all_healthy = False
            except httpx.TimeoutException:
                print(f"{name}: connection timeout")
                all_healthy = False
            except Exception as e:
                print(f"{name}: {str(e)}")
                all_healthy = False
    
    return all_healthy


async def send_task_to_agent(prompt: str, expected_agent: str | None = None):
    """Send a task to the supervisor agent using JSON-RPC 2.0."""
    import httpx
    import uuid
    
    url = "http://localhost:8001"
    
    # JSON-RPC 2.0 format with message/send method
    payload = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "id": str(uuid.uuid4()),
        "params": {
            "message": {
                "messageId": str(uuid.uuid4()),
                "role": "user",
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        }
    }
    
    print(f"\nSending task: {prompt}")
    if expected_agent:
        print(f"Expected to route to: {expected_agent}")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                # Check for JSON-RPC error
                if "error" in result:
                    print(f"Error: {result['error'].get('message', 'Unknown error')}")
                    return False
                
                response_data = result.get("result", {})
                print(f"Response received!")
                
                text_found = False

                if "parts" in response_data and response_data["parts"]:
                    for part in response_data["parts"]:
                        if isinstance(part, dict) and "text" in part:
                            text = part["text"]
                            print(f"\nResponse:\n   {'-'*60}")
                            for line in text.split('\n'):
                                print(f"   {line}")
                            print(f"   {'-'*60}")
                            text_found = True
                            break
                
                # Fallback: check message.parts
                if not text_found and "message" in response_data:
                    msg = response_data["message"]
                    if "parts" in msg and msg["parts"]:
                        for part in msg["parts"]:
                            if isinstance(part, dict) and "text" in part:
                                text = part["text"]
                                print(f"\nResponse:\n   {'-'*60}")
                                for line in text.split('\n'):
                                    print(f"   {line}")
                                print(f"   {'-'*60}")
                                text_found = True
                                break
                
                if not text_found:
                    print(f"Could not extract text from response")
                    print(f"Response structure: {json.dumps(response_data, indent=2)[:500]}")
                
                return True
            else:
                print(f"Failed: HTTP {response.status_code}")
                print(f"{response.text[:200]}")
                return False
                
    except Exception as e:
        print(f"Error: {e}")
        return False



async def test_math_tasks():
    """Test math-related tasks."""
    print("\n" + "="*60)
    print("TESTING MATH AGENT")
    print("="*60)
    
    tasks = [
        "Calculate the area of a circle with radius 7",
        "What is 144 divided by 12?",
        "Calculate the average of these numbers: 10, 20, 30, 40, 50",
    ]
    
    for task in tasks:
        await send_task_to_agent(task, "Math Agent")
        await asyncio.sleep(2)


async def test_coding_tasks():
    """Test coding-related tasks."""
    print("\n" + "="*60)
    print("TESTING CODING AGENT")
    print("="*60)
    
    tasks = [
        "Generate a Python function to calculate fibonacci numbers",
        "Review this code: def add(a,b): return a+b",
        "Help me debug code with a NameError",
    ]
    
    for task in tasks:
        await send_task_to_agent(task, "Coding Agent")
        await asyncio.sleep(2)


async def test_translation_tasks():
    """Test translation-related tasks."""
    print("\n" + "="*60)
    print("TESTING TRANSLATION AGENT")
    print("="*60)
    
    tasks = [
        "Translate 'hello world' to Italian",
        "What language is 'gracias' in?",
        "Translate 'ciao mondo' to English",
    ]
    
    for task in tasks:
        await send_task_to_agent(task, "Translation Agent")
        await asyncio.sleep(2)


async def main():
    """Run all tests."""
    print("MAgNet Supervisor Agent System Tests")
    print("="*60)
    
    # Test connections
    a2a_ok = await test_a2a_connection()
    mcp_ok = await test_mcp_servers()
    
    if not (a2a_ok and mcp_ok):
        print("\nSome services are not ready. Please check the services.")
        return
    
    print("\nAll services are ready!")
    
    # Run task tests
    await test_math_tasks()
    await test_coding_tasks()
    await test_translation_tasks()
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())

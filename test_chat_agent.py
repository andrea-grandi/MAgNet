#!/usr/bin/env python
"""
Test script for the Chat Agent A2A server.
"""
import requests
import json
import uuid

# Server configuration
BASE_URL = "http://localhost:8000"

def test_agent_card():
    """Test getting the agent card"""
    print("=" * 60)
    print("Testing Agent Card...")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/card")
    print(f"Status: {response.status_code}")
    print(f"Agent Card:\n{json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_create_task():
    """Test creating and executing a task"""
    print("=" * 60)
    print("Testing Task Creation and Execution...")
    print("=" * 60)
    
    # Create a task
    task_data = {
        "message": {
            "parts": [
                {
                    "text": "Hello! How are you today?"
                }
            ],
            "role": "user"
        }
    }
    
    context_id = str(uuid.uuid4())
    
    print(f"Creating task with message: 'Hello! How are you today?'")
    response = requests.post(
        f"{BASE_URL}/contexts/{context_id}/messages",
        json=task_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Response:\n{json.dumps(result, indent=2)}\n")
        return True
    else:
        print(f"Error: {response.text}\n")
        return False

def test_streaming():
    """Test streaming responses"""
    print("=" * 60)
    print("Testing Streaming...")
    print("=" * 60)
    
    task_data = {
        "message": {
            "parts": [
                {
                    "text": "Tell me a short joke."
                }
            ],
            "role": "user"
        }
    }
    
    context_id = str(uuid.uuid4())
    
    print(f"Creating streaming task with message: 'Tell me a short joke.'")
    response = requests.post(
        f"{BASE_URL}/contexts/{context_id}/messages",
        json=task_data,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        },
        stream=True
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("Streaming response:")
        for line in response.iter_lines():
            if line:
                print(f"  {line.decode('utf-8')}")
        print()
        return True
    else:
        print(f"Error: {response.text}\n")
        return False

if __name__ == "__main__":
    print("\n🤖 Testing Chat Agent A2A Server\n")
    
    results = []
    
    # Run tests
    results.append(("Agent Card", test_agent_card()))
    results.append(("Task Creation", test_create_task()))
    results.append(("Streaming", test_streaming()))
    
    # Summary
    print("=" * 60)
    print("Test Summary:")
    print("=" * 60)
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print("\n" + "=" * 60)
    total_passed = sum(1 for _, r in results if r)
    print(f"Total: {total_passed}/{len(results)} tests passed")
    print("=" * 60 + "\n")

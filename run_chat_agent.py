#!/usr/bin/env python
"""
Script to run the Chat Agent A2A server.
This ensures proper Python path setup.
"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables FIRST
root_dir = Path(__file__).parent
load_dotenv(root_dir / ".env")

# Add src directory to Python path
src_path = root_dir / "src"
sys.path.insert(0, str(src_path))

# Add chat_agent directory to Python path
chat_agent_path = root_dir / "src" / "magnet" / "agents" / "chat_agent"
sys.path.insert(0, str(chat_agent_path))

# Now we can import and run
from app.__main__ import main
import uvicorn

if __name__ == "__main__":
    host = os.getenv("A2A_HOST", "localhost")
    port = int(os.getenv("A2A_PORT", 8000))
    
    print(f"Starting Chat Agent server on {host}:{port}")
    print(f"OpenAI API Key set: {bool(os.getenv('OPENAI_API_KEY'))}")
    
    app = main()
    uvicorn.run(app, host=host, port=port)

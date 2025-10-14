"""
Main script to test the cooperative swarm of 10 agents.
This script loads the configuration, creates the swarm, and visualizes the graph.
"""

import sys
import os
import yaml
import random

from pathlib import Path
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.globals import set_debug, set_verbose

# Add the magnet module to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from magnet.model import Model
from magnet.agent import Agent
from magnet.tool import Tool
from magnet.handoff import Handoff
from magnet.swarm import Swarm

# Load environment variables
load_dotenv()

set_debug(True)
set_verbose(True)


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    print("🚀 Loading configuration...")
    config = load_config()

    model_name = config["model"]["name"]
    tool_name = config["tools"]["name"]
    tool_docstring = config["tools"]["docstring"]
    agent_name = config["agents"]["name"]
    agent_prompt = config["agents"]["prompt"]
    handoff_description = config["handoffs"]["description"]
    num = config["agents"]["num"]

    # Initialize the model
    print(f"📊 Initializing model: {config['model']['name']}")
    model = Model(model_name)
    llm = model.gpt_4o_mini() 

    tool = Tool(tool_name, tool_docstring, llm)

    handoff = Handoff()
    handoff_list = handoff.create_multiple(agent_name=agent_name, description=handoff_description, num=num)

    #agent = Agent(agent_name, llm, agent_prompt)
    #tools_list = [tool.call]
    #agents = agent.create(tools=tools_list) # type: ignore

    agent = Agent(agent_name, llm, agent_prompt)
    tools_list = [tool.call] + [h for h in handoff_list]
    agents = agent.create_multiple(num=num, tools=tools_list) # type: ignore

    #swarm = Swarm(agents=agents, default_active_agent=agents[0].name) # type: ignore
    swarm = Swarm(agents, agents[random.randint(0,num-1)].name)

    workflow = swarm.create()
    app = workflow.compile()

    image = app.get_graph().draw_mermaid_png()
    with open("swarm.png", "wb") as f:
        f.write(image)

    # Test the swarm
    print("\n🧪 Testing the swarm...")
    test_config = {"configurable": {"thread_id": "test_thread_1"}}
    test_question = "What are the benefits of cooperation in multi-agent systems?"
    
    print(f"\n❓ Question: {test_question}")
    print("\n💬 Swarm response:\n")
    
    try:
        result = app.invoke(
            {"messages": [{"role": "user", "content": test_question}]},
            test_config # type: ignore
        )
        
        # Display all messages
        for msg in result["messages"]:
            print(msg.pretty_print())
            print("-" * 80)
    
    except Exception as e:
        print(f"❌ Error during swarm invocation: {e}")
    
    print("\n✅ Test completed!")
    print("\n" + "="*80)
    print("Swarm is ready for interactive use!")
    print("="*80)
    
    # Interactive mode
    print("\n🔄 Entering interactive mode (type 'exit' to quit)...\n")
    
    while True:
        try:
            user_input = input("\n🗣️  You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Create a new thread for each interaction
            thread_id = f"thread_{hash(user_input)}"
            interactive_config = {"configurable": {"thread_id": thread_id}}
            
            result = swarm.invoke( # type: ignore
                {"messages": [{"role": "user", "content": user_input}]},
                interactive_config # type: ignore
            )
            
            # Display the final response
            final_message = result["messages"][-1]
            print(f"\n🤖 Swarm: {final_message.content}\n")
            print("-" * 80)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()

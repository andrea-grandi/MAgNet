"""
Main script to test the cooperative swarm of 10 agents.
This script loads the configuration, creates the swarm, and visualizes the graph.
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_handoff_tool, create_swarm
import yaml

# Add the magnet module to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from magnet.model import Model
from magnet.agent import Agent
from magnet.tool import Tool
from magnet.handoff import Handoff
from magnet.swarm import Swarm

# Load environment variables
load_dotenv()


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_tool_from_config(tool_config: dict, llm: ChatOpenAI):
    """Create a tool function from configuration."""
    def tool_func(input_text: str) -> str:
        f"""{tool_config['docstring']}"""
        request = tool_config['request'].format(response=input_text)
        response = llm.invoke(request)
        return response.content # type: ignore
    
    tool_func.__name__ = tool_config['name']
    tool_func.__doc__ = tool_config['docstring']
    return tool_func


def main():
    print("🚀 Loading configuration...")
    config = load_config()
    
    # Initialize the model
    print(f"📊 Initializing model: {config['model']['name']}")
    llm = ChatOpenAI(
        model=config['model']['name'],
        temperature=config['model']['temperature']
    )
    
    # Create tools
    print("🔧 Creating tools...")
    tools_map = {}
    for tool_config in config['tools']:
        tool_func = create_tool_from_config(tool_config, llm)
        tools_map[tool_config['name']] = tool_func
    
    # Create handoff tools
    print("🤝 Creating handoff tools...")
    handoff_tools = {}
    for handoff_config in config['handoffs']:
        handoff = Handoff(
            agent_name=handoff_config['agent_name'],
            description=handoff_config['description']
        )
        handoff_tools[handoff_config['agent_name']] = handoff.create()
    
    # Create agents
    print(f"🤖 Creating {len(config['agents'])} cooperative agents...")
    agents_list = []
    
    for agent_config in config['agents']:
        agent_name = agent_config['name']
        
        # Collect tools for this agent
        agent_tools = []
        if 'tools' in agent_config:
            for tool_name in agent_config['tools']:
                if tool_name in tools_map:
                    agent_tools.append(tools_map[tool_name])
        
        # Add handoff tools (all agents can hand off to any other agent)
        for other_agent_name, handoff_tool in handoff_tools.items():
            if other_agent_name != agent_name:  # Don't add self-handoff
                agent_tools.append(handoff_tool)
        
        # Create the agent using langgraph directly
        agent = create_react_agent(
            model=llm,
            tools=agent_tools,
            name=agent_name,
            prompt=agent_config['prompt']
        )
        
        agents_list.append(agent)
        print(f"  ✓ Created {agent_name}")
    
    # Create the swarm
    print("\n🐝 Creating swarm...")
    swarm_config = config['swarm']
    checkpointer = InMemorySaver() if swarm_config.get('checkpointer') == 'memory' else None
    
    swarm_graph = create_swarm(
        agents=agents_list,
        default_active_agent=swarm_config['default_active_agent']
    )
    
    swarm = swarm_graph.compile(checkpointer=checkpointer)
    print(f"  ✓ Swarm created with default agent: {swarm_config['default_active_agent']}")
    
    # Generate and save the graph visualization
    print("\n📸 Generating swarm graph visualization...")
    try:
        image = swarm.get_graph().draw_mermaid_png()
        output_path = "swarm.png"
        with open(output_path, "wb") as f:
            f.write(image)
        print(f"  ✓ Graph saved to: {output_path}")
    except Exception as e:
        print(f"  ⚠️  Error generating graph: {e}")
    
    # Test the swarm
    print("\n🧪 Testing the swarm...")
    test_config = {"configurable": {"thread_id": "test_thread_1"}}
    test_question = "What are the benefits of cooperation in multi-agent systems?"
    
    print(f"\n❓ Question: {test_question}")
    print("\n💬 Swarm response:\n")
    
    try:
        result = swarm.invoke(
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
            
            result = swarm.invoke(
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

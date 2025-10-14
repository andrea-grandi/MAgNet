"""
Main script to test the cooperative swarm of 10 agents.
This script loads the configuration, creates the swarm, and visualizes the graph.
"""

import sys
import random
import yaml
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.globals import set_debug, set_verbose

# Add the magnet module to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from magnet.model import Model
from magnet.agent import Agent
from magnet.handoff import Handoff
from magnet.swarm import Swarm
from magnet.custom import CooperativeAgentOrchestrator, CustomAgentConfig

# Load environment variables
load_dotenv()

set_debug(False)
set_verbose(False)


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    print("🚀 Loading configuration...")
    config = load_config()

    # Extract config
    model_name = config["model"]["name"]
    agent_name = config["agents"]["name"]
    agent_prompt = config["agents"]["prompt"]
    num = config["agents"]["num"]
    handoff_description = config["handoffs"]["description"]
    use_custom = config.get("swarm", {}).get("use_custom", False)
    swarm_cfg = config.get("swarm", {})
    min_before_final = swarm_cfg.get("min_agents_before_final", 3)
    max_turns = swarm_cfg.get("max_turns", None)
    max_chars = swarm_cfg.get("max_chars_per_contribution", None)
    log_dir = swarm_cfg.get("log_dir", None)
    randomize_order = swarm_cfg.get("randomize_order", True)
    single_agent_mode = swarm_cfg.get("single_agent_mode", False)

    # Initialize the model
    print(f"📊 Initializing model: {model_name}")
    model = Model(model_name)
    llm = model.gpt_4o_mini()

    custom_orchestrator = None
    graph_app = None

    if use_custom:
        if single_agent_mode:
            # Override to single agent semantics
            num = 1
            min_before_final = 0
            randomize_order = False

        print("🛠 Using custom cooperative orchestrator (no tool calls, enforced turns)...")
        custom_orchestrator = CooperativeAgentOrchestrator(
            llm=llm,
            config=CustomAgentConfig(
                name_prefix=agent_name,
                num=num,
                min_before_final=min_before_final,
                max_turns=max_turns,
                max_chars_per_contribution=max_chars,
                log_dir=log_dir,
                randomize_order=randomize_order,
            ),
            base_prompt=agent_prompt,
        )
    else:
        handoff = Handoff()
        handoff_list = handoff.create_multiple(agent_name=agent_name, description=handoff_description, num=num)
        agent = Agent(name=agent_name, model=llm, prompt=agent_prompt)
        tools_list = [h for h in handoff_list]
        agents = agent.create_multiple(num=num, tools=tools_list) # type: ignore
        default_agent = agents[random.randint(0, num - 1)].name
        print(f"🎯 Default active agent: {default_agent}")
        swarm = Swarm(agents, default_agent)
        workflow = swarm.create()
        graph_app = workflow.compile()

    if graph_app is not None:
        try:
            image = graph_app.get_graph().draw_mermaid_png()
            with open("swarm.png", "wb") as f:
                f.write(image)
        except Exception as e:
            print(f"❌ Error generating graph image: {e}")

    # Test the swarm
    print("\n🧪 Testing the swarm...")
    test_config = {"configurable": {"thread_id": "test_thread_1"}}
    test_question = "Two circles of radius 1 are centered at $(4,0)$ and $(-4,0).$ How many circles are tangent to both of the given circles and also pass through the point $(0,5)$?"

    
    print(f"\n❓ Question: {test_question}")
    print("\n💬 Swarm response:\n")
    
    try:
        if custom_orchestrator is not None:
            result = custom_orchestrator.run(test_question)
            msgs = result["messages"]
        elif graph_app is not None:
            result = graph_app.invoke(
                {"messages": [{"role": "user", "content": test_question}]},
                test_config # type: ignore
            )
            msgs = result["messages"]
        else:
            raise RuntimeError("No execution backend available.")
        for msg in msgs:
            if hasattr(msg, 'pretty_print'):
                print(msg.pretty_print())
            else:
                role = getattr(msg, 'name', None) or getattr(msg, 'role', 'AI')
                print(f"[{role}] {msg.content}")
            print("-" * 80)

    except Exception as e:
        print(f"❌ Error during swarm invocation: {e}")
    
    print("\n✅ Test completed!")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()

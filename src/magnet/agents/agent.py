from typing import List, Optional, Any, Union, Literal
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph_swarm import create_handoff_tool, create_swarm
from langchain.chat_models import init_chat_model

from magnet.tool import Tool
from magnet.environments import EnvProtocol


class Agent:
    def __init__(
        self, 
        model: str, 
        name: Optional[str],
        wiki: Optional[str],
        tools: Optional[list],
        checkpointer: Optional[Union[InMemorySaver, bool]],
        env: EnvProtocol,
        additional_desc: Optional[str] = "",
        add_forwarding: bool = False,
        strip_handoffs: bool = False,
        handoff_prefix: str = "delegate_to_",
        connectivity: Literal["mesh", "tree"] = "mesh",
    ) -> None:
        """Initialize an agent with the given parameters."""

        self.model = model 
        self.name = name
        self.wiki = wiki
        self.tools = tools
        self.checkpointer = checkpointer
        self.env = env
        self.additional_desc = additional_desc
        self.add_forwarding = add_forwarding
        self.strip_handoffs = strip_handoffs
        self.handoff_prefix = handoff_prefix
        self.connectivity = connectivity
        
    # SINGLE AGENT
    def create_single_agent(
        self,
        wiki: str,
        model: str,
        tools: list,
        checkpointer: InMemorySaver | bool,
        name: str,
        additional_desc: str = "",
    ) -> Any:

        prompt = f"""You are a helpful support assistant.
                    In assisting the user, please comply with the following policies.
                    {wiki}
                    # Instruction
                    You need to act as an agent that use your tools to help the user according to the above policy.
                    Try to be helpful and always follow the policy.{additional_desc}"""  # noqa: E501

        print(f"Constructing agent {name} with {len(tools)} tools")
        agent = create_react_agent(
            model=model,
            prompt=prompt,
            tools=tools,
            checkpointer=checkpointer,
            name=name.replace(" ", "_").lower().strip(),
        )

        return agent
    
    def create_hierarchy(
        self,
        env: EnvProtocol,
        model: str,
        add_forwarding: bool = False,
        strip_handoffs: bool = False,
        handoff_prefix: str = "delegate_to_",
    ) -> Any:
        
        environments = env.environments
        checkpointer = InMemorySaver()
        agents = []
        other_tool = environments[0].tools_map["transfer_to_human_agents"]
        for environment in environments:

            agents.append(
                self.create_single_agent(
                    environment.wiki,
                    model,
                    [
                        t
                        for t in environment.tools_map.values()
                        if t.name != other_tool.name
                    ],
                    True,
                    name=f"{environment.name}_agent".lower().replace(" ", "_").strip(),
                )
            )

        workflow = self.create_supervisor(
            agents,
            model=model,
            prompt=(
                """You are a customer support assistant tasked with helping users.

                # Instructions

                You need to act as a supervisor, routing work to the appropriate agent to take actions or retrieve knowledge. When the agents are finished, they will report back to you with the answer, confirmation of completion, or an error if they run into an issue. 

                You interface with the user. The agents reporting to you cannot. If the other agents have questions or issues, they need you to answer them or relay the information to the user. The user needn't know about the presence of the other agents. You are accountable for the ultimate success of the interaction, including confirmation with your reports around task completion.
                Use all resources available to enable a successful interaction.

                The delegate agent will be able to read the transcript between you and the user. \
                If the delegate responds directly to the user, you can forward it using the forward_message tool.
                Use of the forward_message tool is strongly recommended to save cost and avoid miscommunication."""
            ),
            supervisor_name="support_supervisor",
            handoff_prefix=handoff_prefix,
            tools=[other_tool],
            include_agent_name="inline",
            add_forwarding=add_forwarding,
            strip_handoffs=strip_handoffs,
        )

        return workflow.compile(checkpointer=checkpointer, name="Support Supervisor")
    
    def create_full_swarm(
        self,
        env: EnvProtocol,
        model: str,
        connectivity: Literal["mesh", "tree"] = "mesh",
    ) -> Any:
        environments = env.environments
        checkpointer = InMemorySaver()
        agents = []
        if connectivity not in ("mesh", "tree"):
            raise ValueError(f"Unknown connectivity: {connectivity}")

        def get_name(env):
            return f"{env.name}_agent".lower().replace(" ", "_").strip()

        handoff_tools = {}
        for environment in environments:
            name = get_name(environment)
            handoff_tools[name] = create_handoff_tool(
                agent_name=name,
                description=f"Transfer to {name}, who can help with issues related to {environment.name}",
            )
        router_name = "triage_agent"
        handoff_tools[router_name] = create_handoff_tool(
            agent_name=router_name,
            description="Transfer back up to the top-level triage agent, who can help re-route tasks if "
            "the user switches topics to a domain not covered by you or a similar agent.",
        )
        for environment in environments:
            name = get_name(environment)
            if connectivity == "mesh":
                this_handoffs = [t for a, t in handoff_tools.items() if a != name]
            else:
                this_handoffs = [handoff_tools[router_name]]
            agents.append(
                self.create_single_agent(
                    environment.wiki,
                    model,
                    list(environment.tools_map.values()) + this_handoffs,
                    True,
                    name=name,
                )
            )
        tools = [t for a, t in handoff_tools.items() if a != router_name]

        if model.startswith("google"):
            model_ = init_chat_model(model).bind_tools(tools)
        else:
            model_ = init_chat_model(model).bind_tools(tools, parallel_tool_calls=False)
        first_line = create_react_agent(
            model_,
            tools=tools,
            prompt=(
                """You are a customer support agent tasked with helping users by delegating work to other agents.

                # Instructions

                Act as the initial agent, triaging and routing work to the appropriate agent to satisfy the user's demands.
                If transferring, transfer only to one agent."""
            ),
            name=router_name,
        )

        swarm = create_swarm([first_line, *agents], default_active_agent=router_name)
        return swarm.compile(checkpointer=checkpointer, name="Support Swarm")
    
    def agent_factory(
        self, 
        env: EnvProtocol, 
        agent_strategy: str, 
        model: str
    ) -> Any:
        
        if isinstance(env, str):
            raise ValueError("Environment must be an EnvProtocol, not a string")
        if agent_strategy == "single":
            return self.create_single_agent(
                env.wiki,
                model,
                list(env.tools_map.values()),
                InMemorySaver(),
                name="Support Agent",
            )

        elif agent_strategy == "supervisor":
            return self.create_hierarchy(env, model)
        elif agent_strategy == "supervisor-invisihandoffs":
            return self.create_hierarchy(env, model, strip_handoffs=True)
        elif agent_strategy == "supervisor-forwarding":
            return self.create_hierarchy(env, model, add_forwarding=True)
        elif agent_strategy == "supervisor-forwarding-and-invisihandoffs":
            return self.create_hierarchy(env, model, add_forwarding=True, strip_handoffs=True)
        elif agent_strategy == "supervisor-forwarding-and-invisihandoffs-transfer-prefix":
            return self.create_hierarchy(
                env,
                model,
                add_forwarding=True,
                strip_handoffs=True,
                handoff_prefix="transfer_to_",
            )
        elif agent_strategy == "supervisor-transfer-prefix":
            return self.create_hierarchy(env, model, handoff_prefix="transfer_to_")
        elif agent_strategy == "swarm":
            return self.create_full_swarm(env, model)
        elif agent_strategy == "tree":
            return self.create_full_swarm(env, model, connectivity="tree")
        else:
            raise ValueError(f"Unknown agent strategy: {agent_strategy}")





    
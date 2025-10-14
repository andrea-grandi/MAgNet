from magnet.environment.agents.io import IO
from magnet.environment.agents.tot import TOT
from magnet.environment.agents.cot import COT
from magnet.environment.agents.adversarial_agent import AdversarialAgent
from magnet.environment.agents.agent_registry import AgentRegistry
from magnet.environment.agents.crosswords.tot import CrosswordsToT
from magnet.environment.agents.crosswords.reflection import CrosswordsReflection
from magnet.environment.agents.crosswords.brute_force_opt import CrosswordsBruteForceOpt
from magnet.environment.agents.gaia.tool_io import ToolIO
from magnet.environment.agents.gaia.web_io import WebIO
from magnet.environment.agents.gaia.tool_tot import ToolTOT
from magnet.environment.agents.gaia.normal_io import NormalIO
from magnet.environment.agents.humaneval.code_io import CodeIO
# from magnet.environment.agents.humaneval.code_reflection import CodeReflection

__all__ = [
    "IO",
    "TOT",
    "COT",
    "AdversarialAgent",
    "AgentRegistry",
    "CrosswordsToT",
    "CrosswordsReflection",
    "CrosswordsBruteForceOpt",
    "ToolIO",
    "ToolTOT",
    "NormalIO",
    "WebIO",
    "CodeIO",
]
from magnet.environment.operations.combine_answer import CombineAnswer
from magnet.environment.operations.generate_query import GenerateQuery
from magnet.environment.operations.direct_answer import DirectAnswer
from magnet.environment.operations.file_analyse import FileAnalyse
from magnet.environment.operations.web_search import WebSearch
from magnet.environment.operations.reflect import Reflect
from magnet.environment.operations.final_decision import FinalDecision
from magnet.environment.operations.crosswords.return_all import ReturnAll
from magnet.environment.operations.humaneval.unitest_generation import UnitestGeneration
from magnet.environment.operations.humaneval.code_writing import CodeWriting

__all__ = [
    "CombineAnswer",
    "GenerateQuery",
    "DirectAnswer",
    "FileAnalyse",
    "WebSearch",
    "Reflect",
    "FinalDecision",
    "ReturnAll",
    "UnitestGeneration",
    "CodeWriting",
]
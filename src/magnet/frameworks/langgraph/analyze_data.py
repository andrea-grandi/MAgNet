import sys, os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from magnet.frameworks.prompt_templates.data_analysis_template import PROMPT_TEMPLATE, SYSTEM_PROMPT

load_dotenv()


@tool
def data_analyzer(original_prompt: str, data: str):
    """Provides insights, trends, or analysis based on the data and prompt.

    Args:
        original_prompt (str): The original user prompt that the data is based on.
        data (str): The data to analyze.

    Returns:
        str: The analysis result.
    """
    model = ChatOpenAI(model="gpt-4")
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=PROMPT_TEMPLATE.format(PROMPT=original_prompt, DATA=data)),
    ]
    response = model.invoke(messages)
    return response.content

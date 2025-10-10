#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#sys.path.insert(1, os.path.join(sys.path[0], ".."))

from langchain_openai import ChatOpenAI
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
import warnings
import sys
import io

from magnet.frameworks.db.database import get_schema, get_table
from magnet.frameworks.prompt_templates.router_template import SYSTEM_PROMPT as MANAGER_SYSTEM_PROMPT
from magnet.frameworks.prompt_templates.sql_generator_template import SYSTEM_PROMPT as SQL_SYSTEM_PROMPT
from .sql_query import SQLQueryTool
from .calculator import CalculatorTool

load_dotenv()


def run_crewai(query):
    llm = ChatOpenAI(model="gpt-4o")

    calculator_tool = CalculatorTool()
    sql_query_tool = SQLQueryTool()

    calculator_agent = Agent(
        role="Calculator",
        goal="Perform basic arithmetic operations (+, -, *, /) on two integers.",
        backstory="You are a helpful assistant that can perform basic arithmetic operations (+, -, *, /) "
        "on two integers.",
        tools=[calculator_tool],
        allow_delegation=False,
        verbose=True,
        llm=llm,
    )
    data_analyzer_agent = Agent(
        role="Data Analyzer",
        goal="Provide insights, trends, or analysis based on the data and prompt.",
        backstory="You are a helpful assistant that can provide insights, trends, or analysis based on "
        "the data and prompt.",
        allow_delegation=False,
        verbose=True,
        llm=llm,
    )
    sql_query_agent = Agent(
        role="SQL Query",
        goal="Generate a SQL query based on a user prompt and runs it on the database.",
        backstory=SQL_SYSTEM_PROMPT.format(SCHEMA=get_schema(), TABLE=get_table()),
        tools=[sql_query_tool],
        allow_delegation=False,
        verbose=True,
        llm=llm,
    )

    system_message = (
        "First, identify and make all necessary agent calls based on the user prompt. "
        "Ensure that you gather and aggregate the results from these agent calls. "
        "Once all agent calls are completed and the final result is ready, return it in a single message."
        "If the task is about finding any trends, use the SQL Query Agent first, to retrieve the data "
        "for Data Analyzer Agent."
    )
    manager_agent = Agent(
        role="Manager",
        goal=system_message,
        backstory=MANAGER_SYSTEM_PROMPT,
        allow_delegation=True,
        verbose=True,
        llm=llm,
    )

    # Extract goals and constraints from query if present
    expected_output = (
        "Once all agent calls are completed and the final result is ready, return it "
        "in a single message. If the task includes specific goals and constraints, "
        "your final response should include:\n"
        "1. A clear plan or solution\n"
        "2. Which goals were achieved (list the exact goal descriptions)\n"
        "3. Which constraints were satisfied (list the exact constraint descriptions)\n"
        "Format your response as JSON if the query contains structured goals/constraints, otherwise provide a clear text response."
    )
    
    user_query_task = Task(
        name="user_query_task",
        description=query,
        expected_output=expected_output,
        agent=manager_agent,
    )

    crew = Crew(
        agents=[calculator_agent, data_analyzer_agent, sql_query_agent],
        tasks=[user_query_task],
        process=Process.sequential,
        manager_agent=manager_agent,
    )
    
    # Suppress EventBus error messages (known CrewAI internal issue)
    # The error "[EventBus Error] Handler 'on_task_started' failed" is a harmless
    # warning in CrewAI 0.203.0 when using hierarchical process
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    
    try:
        result = crew.kickoff()
    finally:
        # Restore stderr
        captured = sys.stderr.getvalue()
        sys.stderr = old_stderr
        # Only print non-EventBus errors
        if captured and "[EventBus Error]" not in captured:
            sys.stderr.write(captured)
    
    return result.raw

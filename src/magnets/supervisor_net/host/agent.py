from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

# Define LiteLlm models
myModel = LiteLlm(model="openai/gpt-4o-mini") # Must specify the model name

# We have created a single agent using LiteLlm
root_agent = Agent(
    model=myModel,
    name="LiteAgent",
    description="A minimal agent that takes input and produces a simple output using a lightweight model.",
    instruction="""
    You are a basic assistant that takes a topic and generates a short social media post about it.
    Keep it concise, relevant, and easy to understand.
    """
)
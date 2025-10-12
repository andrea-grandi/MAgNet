"""LLM models configuration."""

from langchain_openai import ChatOpenAI

# Default model for agents
GPT_4O_MINI = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
GPT_4O = ChatOpenAI(model="gpt-4o", temperature=0.7)

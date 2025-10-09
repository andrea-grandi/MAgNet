from langchain_openai import ChatOpenAI

from magnet.configs.llm_config import DEFAULT_LLM_CONFIG

llm = ChatOpenAI(**DEFAULT_LLM_CONFIG)

chain = llm
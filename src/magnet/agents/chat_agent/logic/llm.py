from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from magnet.configs.llm_config import *


llm = ChatOpenAI(**CHAT_AGENT_CONFIG)
system_prompt = ChatPromptTemplate.from_messages(CHAT_AGENT_SYSTEM_PROMPT)
model = system_prompt | llm
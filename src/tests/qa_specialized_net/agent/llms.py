

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()  


GPT_4O_MINI = ChatOpenAI(
    model="gpt-4o-mini",
)
# LLM configurations for different agents
CHAT_AGENT_CONFIG = {
    "model": "gpt-4o-mini",
    "temperature": 1.0,
    "max_tokens": 2048,
}

CRITIC_AGENT_CONFIG = {
    "model": "gpt-4o",
    "temperature": 0.0,
    "max_tokens": 1024,
}

CODING_AGENT_CONFIG = {
    "model": "gpt-4o",
    "temperature": 0.2,
    "max_tokens": 2048,
}

# System prompts for different agents
CHAT_AGENT_SYSTEM_PROMPT = "You are a helpful AI assistant."
CRITIC_AGENT_SYSTEM_PROMPT = "You are a meticulous code reviewer."
CODING_AGENT_SYSTEM_PROMPT = "You are an expert programmer."

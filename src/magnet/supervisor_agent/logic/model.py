from langchain_openai import ChatOpenAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint 
from langchain_ollama import ChatOllama


def get_model(model_name: str):
    """Get the language model instance."""

    # HuggigFace models
    if model_name == "meta-llama/Llama-3.1-8B-Instruct":
        llm = HuggingFaceEndpoint(
            repo_id=model_name,
            task="text-generation",
            max_new_tokens=1024,
            do_sample=False,
            repetition_penalty=1.03,
            provider="auto"
        )
        return ChatHuggingFace(llm=llm)
    
    # OpenAI models
    elif model_name.startswith("gpt-"):
        return ChatOpenAI(name=model_name)
    
    # Ollama models
    elif model_name.startswith("ollama-"):
        return ChatOllama(
            model=model_name, 
            temperature=0.0,
            max_tokens=1024
        )
    
    else:
        raise ValueError(f"Unsupported model: {model_name}")

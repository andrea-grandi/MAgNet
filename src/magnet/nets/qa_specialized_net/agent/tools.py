
from .llms import GPT_4O_MINI


def question_answering(request: str):
    """General Question Answering Agent

    Handles non-scientific, general knowledge questions.
    Transfers science questions to science_agent and translation requests to translator_agent.

    Args:
        question (str): The user's question

    Returns:
        str: Response from the language model
    """
    response = GPT_4O_MINI.invoke(request)
    return response.content

def science_agent(request: str):
    """Science Specialist Agent

    Handles questions about physics, chemistry, biology, astronomy, and other scientific topics.
    Transfers non-science questions to question_answering_agent and translation requests to translator_agent.

    Args:
        question (str): The science-related question

    Returns:
        str: Scientific explanation or answer
    """
    response = GPT_4O_MINI.invoke(request)
    return response.content

def extract_language_and_text(request: str):
    """Extract target language and text from a translation request

    Parses the user's request to identify:
    1. The text to be translated
    2. The target language for translation

    Handles various formats:
    - "translate X to Y"
    - "X in Y"
    - "X into Y"

    Args:
        request (str): The user's translation request

    Returns:
        tuple: (text_to_translate, target_language)
    """
    request = request.lower()

    # Common language patterns
    to_patterns = [" to ", " in ", " into "]

    # Try to find language in the request
    target_language = None
    text = request

    for pattern in to_patterns:
        if pattern in request:
            parts = request.split(pattern)
            if len(parts) == 2:
                text = parts[0]
                # Take everything after the pattern as language
                target_language = parts[1].strip()
                break

    # Clean up text by removing translation-related prefixes
    text = text.replace("translate", "").replace("say", "").strip()
    return text.strip(), target_language

def translate_text(request: str):
    """Translation Handler

    Processes translation requests in various formats:
    1. Direct translation with language: "translate X to Y"
    2. Help requests: "help with translation"
    3. Text-only requests: Prompts for target language

    Args:
        request (str): The translation request or text to translate

    Returns:
        str: Either translation instructions or the translated text
    """
    # If it's a help request, provide format guidance
    if any(x in request.lower() for x in ["help with", "can you", "need translation", "translate something"]):
        return "I can help you translate. Please provide what you want to translate using this format:\n'translate [your text] to [language]' or '[text] in [language]'"

    # Try to extract language and text
    text, target_language = extract_language_and_text(request)

    # If language wasn't found in the request, ask for it
    if not target_language:
        target_language = input("Which language would you like this translated to? ")

    prompt = f"Translate the following text to {target_language}:\n{text}"
    response = GPT_4O_MINI.invoke(prompt)
    return response.content


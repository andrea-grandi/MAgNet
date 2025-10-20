"""Business logic for translation operations."""

from .models import (
    TranslateInput,
    TranslateOutput,
    DetectLanguageInput,
    DetectLanguageOutput,
    SupportedLanguagesOutput
)


# Simple language database
LANGUAGES = {
    "en": "English",
    "it": "Italian",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
}

# Simple translation examples for demonstration
TRANSLATION_EXAMPLES = {
    ("en", "it"): {
        "hello": "ciao",
        "world": "mondo",
        "goodbye": "arrivederci",
        "thank you": "grazie",
        "please": "per favore",
        "yes": "sì",
        "no": "no",
    },
    ("it", "en"): {
        "ciao": "hello",
        "mondo": "world",
        "arrivederci": "goodbye",
        "grazie": "thank you",
        "per favore": "please",
        "sì": "yes",
        "no": "no",
    },
    ("en", "es"): {
        "hello": "hola",
        "world": "mundo",
        "goodbye": "adiós",
        "thank you": "gracias",
        "please": "por favor",
        "yes": "sí",
        "no": "no",
    },
    ("es", "en"): {
        "hola": "hello",
        "mundo": "world",
        "adiós": "goodbye",
        "gracias": "thank you",
        "por favor": "please",
        "sí": "yes",
        "no": "no",
    },
}


def detect_language(req: DetectLanguageInput) -> DetectLanguageOutput:
    """Detect the language of the text."""
    
    text_lower = req.text.lower()
    
    # Simple heuristic-based detection
    italian_words = ["ciao", "grazie", "arrivederci", "mondo", "per favore"]
    spanish_words = ["hola", "gracias", "adiós", "mundo", "por favor"]
    english_words = ["hello", "thank", "goodbye", "world", "please"]
    
    italian_count = sum(1 for word in italian_words if word in text_lower)
    spanish_count = sum(1 for word in spanish_words if word in text_lower)
    english_count = sum(1 for word in english_words if word in text_lower)
    
    if italian_count > spanish_count and italian_count > english_count:
        language = "it"
        confidence = 0.85
    elif spanish_count > english_count:
        language = "es"
        confidence = 0.80
    else:
        language = "en"
        confidence = 0.75
    
    return DetectLanguageOutput(
        language=language,
        language_name=LANGUAGES.get(language, "Unknown"),
        confidence=confidence
    )


def translate_text(req: TranslateInput) -> TranslateOutput:
    """Translate text from source to target language."""
    
    source_lang = req.source_language
    
    # Auto-detect source language if needed
    if source_lang == "auto":
        detection = detect_language(DetectLanguageInput(text=req.text))
        source_lang = detection.language
    
    # Validate languages
    if source_lang not in LANGUAGES:
        source_lang = "en"
    if req.target_language not in LANGUAGES:
        raise ValueError(f"Unsupported target language: {req.target_language}")
    
    # If source and target are the same
    if source_lang == req.target_language:
        return TranslateOutput(
            translated_text=req.text,
            source_language=source_lang,
            target_language=req.target_language,
            confidence=1.0
        )
    
    # Get translation pair
    translation_key = (source_lang, req.target_language)
    translations = TRANSLATION_EXAMPLES.get(translation_key, {})
    
    # Simple word-by-word translation
    text_lower = req.text.lower().strip()
    
    if text_lower in translations:
        translated_text = translations[text_lower]
        confidence = 0.95
    else:
        # For unknown phrases, provide a template response
        translated_text = f"[Translation from {LANGUAGES[source_lang]} to {LANGUAGES[req.target_language]}]: {req.text}"
        confidence = 0.60
    
    # Preserve capitalization
    if req.text and req.text[0].isupper():
        translated_text = translated_text.capitalize()
    
    return TranslateOutput(
        translated_text=translated_text,
        source_language=source_lang,
        target_language=req.target_language,
        confidence=confidence
    )


def get_supported_languages() -> SupportedLanguagesOutput:
    """Get list of supported languages."""
    
    languages = [
        {"code": code, "name": name}
        for code, name in LANGUAGES.items()
    ]
    
    return SupportedLanguagesOutput(languages=languages)

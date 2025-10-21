from pydantic import BaseModel, Field
from typing import List, Optional


class TranslateInput(BaseModel):
    """Input for text translation."""
    text: str = Field(..., description="Text to translate")
    source_language: str = Field(default="auto", description="Source language code (e.g., 'en', 'it', 'es')")
    target_language: str = Field(..., description="Target language code (e.g., 'en', 'it', 'es')")
    
    
class TranslateOutput(BaseModel):
    """Output for text translation."""
    translated_text: str = Field(..., description="Translated text")
    source_language: str = Field(..., description="Detected/specified source language")
    target_language: str = Field(..., description="Target language")
    confidence: float = Field(..., description="Translation confidence (0-1)")


class DetectLanguageInput(BaseModel):
    """Input for language detection."""
    text: str = Field(..., description="Text to analyze")
    
    
class DetectLanguageOutput(BaseModel):
    """Output for language detection."""
    language: str = Field(..., description="Detected language code")
    language_name: str = Field(..., description="Full language name")
    confidence: float = Field(..., description="Detection confidence (0-1)")


class SupportedLanguagesOutput(BaseModel):
    """Output for supported languages list."""
    languages: List[dict] = Field(..., description="List of supported languages with codes and names")

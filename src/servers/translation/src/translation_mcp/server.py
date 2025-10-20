"""FastMCP server for translation operations."""

import os
import logging

from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from dotenv import load_dotenv

from .models import (
    TranslateInput,
    TranslateOutput,
    DetectLanguageInput,
    DetectLanguageOutput,
    SupportedLanguagesOutput
)
from .logic import translate_text, detect_language, get_supported_languages

logger = logging.getLogger(__name__)

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

HOST = os.getenv("MCP_HOST", "localhost")
PORT = int(os.getenv("MCP_PORT", "8992"))

mcp = FastMCP(
    name="translation_mcp",
    instructions=(
        "This MCP provides tools for text translation and language detection. "
        "It supports multiple languages and can automatically detect source language."
    ),
)


@mcp.tool
def translate_tool(ctx: Context, req: TranslateInput) -> TranslateOutput:
    """Translate text from one language to another."""
    
    try:
        return translate_text(req)
    except Exception as e:
        logger.info(f"Exception in translation: {e}")
        raise ToolError(str(e))


@mcp.tool
def detect_language_tool(ctx: Context, req: DetectLanguageInput) -> DetectLanguageOutput:
    """Detect the language of a given text."""
    
    try:
        return detect_language(req)
    except Exception as e:
        logger.info(f"Exception in language detection: {e}")
        raise ToolError(str(e))


@mcp.tool
def supported_languages_tool(ctx: Context) -> SupportedLanguagesOutput:
    """Get list of all supported languages."""
    
    try:
        return get_supported_languages()
    except Exception as e:
        logger.info(f"Exception in getting supported languages: {e}")
        raise ToolError(str(e))


@mcp.tool
def health_check() -> dict:
    """Health check endpoint for Docker"""
    
    return {"status": "healthy", "service": "translation-mcp"}


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host=HOST, port=PORT, path="/mcp")

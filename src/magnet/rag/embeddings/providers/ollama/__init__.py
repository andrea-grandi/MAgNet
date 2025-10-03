"""Ollama embedding providers."""

from magnet.rag.embeddings.providers.ollama.ollama_provider import (
    OllamaProvider,
)
from magnet.rag.embeddings.providers.ollama.types import (
    OllamaProviderConfig,
    OllamaProviderSpec,
)

__all__ = [
    "OllamaProvider",
    "OllamaProviderConfig",
    "OllamaProviderSpec",
]

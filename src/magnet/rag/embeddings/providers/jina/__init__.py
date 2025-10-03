"""Jina embedding providers."""

from magnet.rag.embeddings.providers.jina.jina_provider import JinaProvider
from magnet.rag.embeddings.providers.jina.types import (
    JinaProviderConfig,
    JinaProviderSpec,
)

__all__ = [
    "JinaProvider",
    "JinaProviderConfig",
    "JinaProviderSpec",
]

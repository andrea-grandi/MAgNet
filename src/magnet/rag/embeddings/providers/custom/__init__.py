"""Custom embedding providers."""

from magnet.rag.embeddings.providers.custom.custom_provider import CustomProvider
from magnet.rag.embeddings.providers.custom.types import (
    CustomProviderConfig,
    CustomProviderSpec,
)

__all__ = [
    "CustomProvider",
    "CustomProviderConfig",
    "CustomProviderSpec",
]

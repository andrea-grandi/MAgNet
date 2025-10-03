"""Microsoft embedding providers."""

from magnet.rag.embeddings.providers.microsoft.azure import (
    AzureProvider,
)
from magnet.rag.embeddings.providers.microsoft.types import (
    AzureProviderConfig,
    AzureProviderSpec,
)

__all__ = [
    "AzureProvider",
    "AzureProviderConfig",
    "AzureProviderSpec",
]

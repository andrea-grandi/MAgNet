"""IBM embedding providers."""

from magnet.rag.embeddings.providers.ibm.types import (
    WatsonProviderSpec,
    WatsonXProviderConfig,
    WatsonXProviderSpec,
)
from magnet.rag.embeddings.providers.ibm.watsonx import (
    WatsonXProvider,
)

__all__ = [
    "WatsonProviderSpec",
    "WatsonXProvider",
    "WatsonXProviderConfig",
    "WatsonXProviderSpec",
]

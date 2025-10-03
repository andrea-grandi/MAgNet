"""HuggingFace embedding providers."""

from magnet.rag.embeddings.providers.huggingface.huggingface_provider import (
    HuggingFaceProvider,
)
from magnet.rag.embeddings.providers.huggingface.types import (
    HuggingFaceProviderConfig,
    HuggingFaceProviderSpec,
)

__all__ = [
    "HuggingFaceProvider",
    "HuggingFaceProviderConfig",
    "HuggingFaceProviderSpec",
]

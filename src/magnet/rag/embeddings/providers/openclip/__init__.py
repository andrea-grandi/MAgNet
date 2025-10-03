"""OpenCLIP embedding providers."""

from magnet.rag.embeddings.providers.openclip.openclip_provider import (
    OpenCLIPProvider,
)
from magnet.rag.embeddings.providers.openclip.types import (
    OpenCLIPProviderConfig,
    OpenCLIPProviderSpec,
)

__all__ = [
    "OpenCLIPProvider",
    "OpenCLIPProviderConfig",
    "OpenCLIPProviderSpec",
]

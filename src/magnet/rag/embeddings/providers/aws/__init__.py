"""AWS embedding providers."""

from magnet.rag.embeddings.providers.aws.bedrock import BedrockProvider
from magnet.rag.embeddings.providers.aws.types import (
    BedrockProviderConfig,
    BedrockProviderSpec,
)

__all__ = [
    "BedrockProvider",
    "BedrockProviderConfig",
    "BedrockProviderSpec",
]

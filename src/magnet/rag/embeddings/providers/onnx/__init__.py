"""ONNX embedding providers."""

from magnet.rag.embeddings.providers.onnx.onnx_provider import ONNXProvider
from magnet.rag.embeddings.providers.onnx.types import (
    ONNXProviderConfig,
    ONNXProviderSpec,
)

__all__ = [
    "ONNXProvider",
    "ONNXProviderConfig",
    "ONNXProviderSpec",
]

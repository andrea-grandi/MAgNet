"""Type definitions for the embeddings module."""

from typing import Literal, TypeAlias

from magnet.rag.core.base_embeddings_provider import BaseEmbeddingsProvider
from magnet.rag.embeddings.providers.aws.types import BedrockProviderSpec
from magnet.rag.embeddings.providers.cohere.types import CohereProviderSpec
from magnet.rag.embeddings.providers.custom.types import CustomProviderSpec
from magnet.rag.embeddings.providers.google.types import (
    GenerativeAiProviderSpec,
    VertexAIProviderSpec,
)
from magnet.rag.embeddings.providers.huggingface.types import HuggingFaceProviderSpec
from magnet.rag.embeddings.providers.ibm.types import (
    WatsonProviderSpec,
    WatsonXProviderSpec,
)
from magnet.rag.embeddings.providers.instructor.types import InstructorProviderSpec
from magnet.rag.embeddings.providers.jina.types import JinaProviderSpec
from magnet.rag.embeddings.providers.microsoft.types import AzureProviderSpec
from magnet.rag.embeddings.providers.ollama.types import OllamaProviderSpec
from magnet.rag.embeddings.providers.onnx.types import ONNXProviderSpec
from magnet.rag.embeddings.providers.openai.types import OpenAIProviderSpec
from magnet.rag.embeddings.providers.openclip.types import OpenCLIPProviderSpec
from magnet.rag.embeddings.providers.roboflow.types import RoboflowProviderSpec
from magnet.rag.embeddings.providers.sentence_transformer.types import (
    SentenceTransformerProviderSpec,
)
from magnet.rag.embeddings.providers.text2vec.types import Text2VecProviderSpec
from magnet.rag.embeddings.providers.voyageai.types import VoyageAIProviderSpec

ProviderSpec = (
    AzureProviderSpec
    | BedrockProviderSpec
    | CohereProviderSpec
    | CustomProviderSpec
    | GenerativeAiProviderSpec
    | HuggingFaceProviderSpec
    | InstructorProviderSpec
    | JinaProviderSpec
    | OllamaProviderSpec
    | ONNXProviderSpec
    | OpenAIProviderSpec
    | OpenCLIPProviderSpec
    | RoboflowProviderSpec
    | SentenceTransformerProviderSpec
    | Text2VecProviderSpec
    | VertexAIProviderSpec
    | VoyageAIProviderSpec
    | WatsonProviderSpec  # Deprecated, use WatsonXProviderSpec
    | WatsonXProviderSpec
)

AllowedEmbeddingProviders = Literal[
    "azure",
    "amazon-bedrock",
    "cohere",
    "custom",
    "google-generativeai",
    "google-vertex",
    "huggingface",
    "instructor",
    "jina",
    "ollama",
    "onnx",
    "openai",
    "openclip",
    "roboflow",
    "sentence-transformer",
    "text2vec",
    "voyageai",
    "watsonx",
    "watson",  # for backward compatibility until v1.0.0
]

EmbedderConfig: TypeAlias = (
    ProviderSpec | BaseEmbeddingsProvider | type[BaseEmbeddingsProvider]
)

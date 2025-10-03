"""Instructor embedding providers."""

from magnet.rag.embeddings.providers.instructor.instructor_provider import (
    InstructorProvider,
)
from magnet.rag.embeddings.providers.instructor.types import (
    InstructorProviderConfig,
    InstructorProviderSpec,
)

__all__ = [
    "InstructorProvider",
    "InstructorProviderConfig",
    "InstructorProviderSpec",
]

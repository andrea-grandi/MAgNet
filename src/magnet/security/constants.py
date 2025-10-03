"""Security constants for NetAI.

This module contains security-related constants used throughout the security module.

Notes:
    - TODO: Determine if MAGNET_AI_NAMESPACE should be made dynamic or configurable
"""

from typing import Annotated
from uuid import UUID

MAGNET_AI_NAMESPACE: Annotated[
    UUID,
    "Create a deterministic UUID using v5 (SHA-1). Custom namespace for MAgNet to enhance security.",
] = UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479")

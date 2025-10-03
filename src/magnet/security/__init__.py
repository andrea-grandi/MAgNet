"""

This module provides security-related functionality for MAgNet, including:
- Fingerprinting for component identity and tracking
- Security configuration for controlling access and permissions
- Future: authentication, scoping, and delegation mechanisms
"""

from magnet.security.fingerprint import Fingerprint
from magnet.security.security_config import SecurityConfig

__all__ = ["Fingerprint", "SecurityConfig"]

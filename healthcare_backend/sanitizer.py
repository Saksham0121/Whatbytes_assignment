"""
Shared sanitization utility used across all serializers.

Uses bleach with a strict zero-tolerance policy: ALL HTML tags and
attributes are stripped. This prevents stored XSS attacks.
"""

import bleach


def sanitize(value):
    """
    Strip ALL HTML tags, attributes, and null bytes from the input string.
    Returns a clean plain-text string.
    """
    if not isinstance(value, str):
        return value
    cleaned = value.replace("\x00", "").strip()
    return bleach.clean(cleaned, tags=[], attributes={}, strip=True)

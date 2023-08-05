"""Helper utilities for various faker providers."""

from random import choice


def _choice_str(choices, max):
    """Generate a string up to a given length from provided random choices."""
    return ''.join(map(str, [choice(choices) for _ in range(max)]))

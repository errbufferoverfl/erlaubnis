"""
Global validators and sanitisers used to keep data reasonable & secure.

For validators and sanitisers specific to each model check out their associated validators file:
"""
from typing import Any

import bleach


def sanitize_string(user_input: str):
    """

    Args:
        user_input:

    Returns:

    """
    try:
        return bleach.clean(user_input, strip=True)
    except TypeError:
        raise


def sanitize_dictionary(**kwargs):
    for key, value in kwargs.items():
        if key != "password_hash":
            try:
                kwargs[key] = sanitize_string(value)
            except TypeError:
                continue

    return kwargs


def blank(value: Any) -> bool:
    if isinstance(value, str):
        if value.isspace():
            return True
        if len(value) < 1:
            return True


def not_null(value: Any):
    if value:
        return True

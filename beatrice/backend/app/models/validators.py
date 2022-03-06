"""Validation utility functions for models."""


def normalize_name(name: str) -> str:
    """Capitalizes every word in a name.

    Params:
        name: The name to normalize.

    Returns:
        The normalized name.
    """
    return " ".join((word.capitalize()) for word in name.split(" "))


def normalize_title(title: str) -> str:
    """Capitalizes the title.

    Params:
        title: The title to normalize.

    Returns:
        The normalized title.
    """
    return title.strip().capitalize()

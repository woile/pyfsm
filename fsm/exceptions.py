__all__ = ["InvalidTransition", "AbortTransition"]


class InvalidTransition(Exception):
    """Moving from an state to another is not possible."""

    pass


class AbortTransition(Exception):
    """Changing state should be aborted"""

    pass

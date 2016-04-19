__all__ = ['InvalidTransition']


class InvalidTransition(Exception):
    """Moving from an state to another is not possible."""
    pass

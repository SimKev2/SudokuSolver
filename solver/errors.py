class CantSolveError(Exception):
    """Raised by the bruteforce algorithm if it cannot solve the board."""


class ConflictError(Exception):
    """Raised when an update is attempted but a value conflict exists."""

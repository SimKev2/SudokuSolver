"""Module for methods related to a single cell in board."""


class Cell:
    """An individual cell in a board."""

    def __init__(self, values: [int]):
        """
        Initialize a cell.

        :param values: Values the cell could be, defaults to all nums 1-9.
        """
        self.values = values or list(range(1,10))

    @property
    def settled(self) -> bool:
        """If cell value is known."""
        return len(self.values) == 1

    def __eq__(self, other):
        """Equality override."""
        if type(other) is type(self):
            return self.values == other.values

        return False

    def __repr__(self):
        """Representation of the cell, either the singular value or "_"."""
        return str(self.values[0]) if self.settled else '_'

    def __str__(self):
        """The str representation of the cell."""
        return self.__repr__()

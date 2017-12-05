"""Methods related to the Sudoku board."""
import copy

from .cell import Cell
from .errors import CantSolveError, ConflictError


class Board:
    """A 9x9 Sudoku board."""

    def __init__(self, board_string: str):
        """
        Initialize a board.

        :param board_string: A string representation of a Sudoku board, where
            the characters in the string go from top left corner, across the
            row, then down one row. Where a number is a filled cell and a dot
            is any possible number, i.e. the first row may be "1.7....4."
        """
        assert len(board_string) == 81, 'Board must be 81 chars for 9x9'
        self.board = []  # Addressed as [row][col]
        for row in range(9):
            self.board.append([None] * 9)
            for col in range(9):
                try:
                    self.board[row][col] = Cell([int(board_string[row*9+col])])
                except ValueError:
                    self.board[row][col] = Cell([])

    @property
    def cells(self) -> [Cell]:
        """Return a list of all cells in the board in index order."""
        return [c for row in self.board for c in row]

    @property
    def solved(self) -> bool:
        """Return True if all cells are settled."""
        return all(cell.settled for cell in self.cells)

    def __repr__(self):
        """Draw Sudoku board."""
        row_repr = '{:2}{:2}{:2}| {:2}{:2}{:2}| {:2}{:2}{:2}\n'
        board_repr = ''
        for line_break in range(3):
            for row in range(3):
                board_repr += row_repr.format(*map(str, self.row_of(
                    line_break * 27 + row * 9)))

            board_repr += '---------------------\n' if line_break < 2 else ''

        return board_repr

    def __str__(self):
        return self.__repr__()

    def col_of(self, index: int) -> [Cell]:
        """Return a list of the cells in the same col as index (0-80)."""
        return [row[index % 9] for row in self.board]

    def minigrid_of(self, index: int) -> [Cell]:
        """Return a list of the cells in the same mini grid as index (0-80)."""
        row_offset = (index // 9) % 3
        col_offset = index % 3
        col_index_start = index % 9 - col_offset

        top_left = index - col_offset - row_offset * 9
        grid = []
        for row_num in range(3):
            grid.extend(self.row_of(
                top_left + row_num * 9)[col_index_start:col_index_start + 3])

        return grid

    def row_of(self, index: int) -> [Cell]:
        """Return a list of the cells in the same row as index (0-80)."""
        return self.board[index // 9]

    def can_update(self, index: int, value: int) -> bool:
        """Assert if the cell at index can be updated to the singular value."""
        known_values = [c.values[0] for c in self.row_of(index) if c.settled]
        known_values.extend(
            c.values[0] for c in self.col_of(index) if c.settled)
        known_values.extend(
            c.values[0] for c in self.minigrid_of(index) if c.settled)

        return value not in known_values

    def update(self, index: int, values: [int]) -> None:
        """
        Updates the cell values at index with values.

        If values is a list of one integer, can_update is checked.
        :raises ConflictError: If the cell at index cannot be updated to the
            given singular value.
        """
        if len(values) == 1:
            if not self.can_update(index, values[0]):
                raise ConflictError()

        self.cells[index].values = values

    def solve(self) -> None:
        """Solve and print the Sudoku puzzle board."""
        while not self.solved:
            unchanged = True
            for index, cell in enumerate(self.cells):
                if cell.settled:
                    continue

                possible_values = [
                    val for val in cell.values if self.can_update(index, val)]

                if not possible_values:
                    raise CantSolveError()

                if cell.values != possible_values:
                    self.update(index, possible_values)
                    unchanged = False

            if unchanged:
                choices = sorted(enumerate(
                    self.cells), key=lambda c: len(c[1].values))

                choice_index, choice_cell = next((
                    cell for cell in choices if not cell[1].settled), None)

                for v in choice_cell.values:
                    new_board = copy.deepcopy(self)
                    new_board.update(choice_index, [v])

                    try:
                        return new_board.solve()
                    except CantSolveError:
                        continue

                raise CantSolveError()

        print(self)

import math
from unittest import TestCase

from .. import board


class BoardBaseCase(TestCase):
    def setUp(self):
        board_str = (
            '..3.2.6..'
            '9..3.5..1'
            '..18.64..'
            '..81.29..'
            '7.......8'
            '..67.82..'
            '..26.95..'
            '8..2.3..9'
            '..5.1.3..')

        self.test_board = board.Board(board_str)
        self.columns = [
            [None] * 9,
            [None] * 9,
            [None] * 9,
            [None] * 9,
            [None] * 9,
            [None] * 9,
            [None] * 9,
            [None] * 9,
            [None] * 9]  # Avoid list references
        self.rows = []
        self.minigrids = [[], [], [], [], [], [], [], [], []]

        for r in range(9):
            self.rows.append([None] * 9)
            for c in range(9):
                index = r * 9 + c
                mini_row = int(math.floor(index // 9 / 3))  # 0, 1, 2
                mini_col = int(math.floor(index % 9 / 3))  # 0, 1, 2
                try:
                    cell_val = int(board_str[index])
                    self.rows[r][c] = board.Cell([cell_val])
                    self.columns[c][r] = board.Cell([cell_val])
                    self.minigrids[mini_row * 3 + mini_col].append(board.Cell(
                        [cell_val]))

                except ValueError:
                    self.rows[r][c] = board.Cell([])
                    self.columns[c][r] = board.Cell([])
                    self.minigrids[mini_row * 3 + mini_col].append(
                        board.Cell([]))


class InitCellsTestCase(BoardBaseCase):
    def test_board_cells(self):
        settled_num = 0

        for c in self.test_board.cells:
            self.assertTrue(isinstance(c, board.Cell))
            if c.settled:
                settled_num += 1

        self.assertEqual(32, settled_num)


class SolvedTestCase(BoardBaseCase):
    def test_not_solved(self):
        self.assertFalse(self.test_board.solved)

    def test_solved(self):
        solved_board = board.Board('1'*81)
        self.assertTrue(solved_board.solved)


class RowOfTestCase(BoardBaseCase):
    def test_row_of(self):
        for i in range(81):
            self.assertEqual(self.rows[i // 9], self.test_board.row_of(i))


class ColOfTestCase(BoardBaseCase):
    def test_col_of(self):
        for r in range(9):
            for c in range(9):
                self.assertEqual(
                    self.columns[c], self.test_board.col_of(r * 9 + c))


class MinigridOfTestCase(BoardBaseCase):
    def test_minigrid_of(self):
        mini_grid_indexes = [
            [0, 1, 2, 9, 10, 11, 18, 19, 20],
            [3, 4, 5, 12, 13, 14, 21, 22, 23],
            [6, 7, 8, 15, 16, 17, 24, 25, 26],
            [27, 28, 29, 36, 37, 38, 45, 46, 47],
            [30, 31, 32, 39, 40, 41, 48, 49, 50],
            [33, 34, 35, 42, 43, 44, 51, 52, 53],
            [54, 55, 56, 63, 64, 65, 72, 73, 74],
            [57, 58, 59, 66, 67, 68, 75, 76, 77],
            [60, 61, 62, 69, 70, 71, 78, 79, 80]]

        for mg, indexes in enumerate(mini_grid_indexes):
            for i in indexes:
                self.assertEqual(
                    self.minigrids[mg], self.test_board.minigrid_of(i))


class CanUpdateTestCase(BoardBaseCase):
    def test_can_update(self):
        self.assertTrue(self.test_board.can_update(40, 3))
        self.assertTrue(self.test_board.can_update(40, 4))
        self.assertTrue(self.test_board.can_update(40, 5))
        self.assertTrue(self.test_board.can_update(40, 6))
        self.assertTrue(self.test_board.can_update(40, 9))

    def test_cant_update(self):
        self.assertFalse(self.test_board.can_update(40, 1))
        self.assertFalse(self.test_board.can_update(40, 2))
        self.assertFalse(self.test_board.can_update(40, 7))
        self.assertFalse(self.test_board.can_update(40, 8))

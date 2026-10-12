import unittest
from board import Board
from rules import valid_move, parse_move


class TestDotsAndBoxes(unittest.TestCase):

    def setUp(self):
        self.board = Board(rows=2, cols=2)

    def test_valid_horizontal_move(self):
        self.assertTrue(valid_move(self.board, "H", 0, 0))
        self.board.add_line("H", 0, 0, player=0)
        self.assertTrue(self.board.horizontal[0][0])

    def test_valid_vertical_move(self):
        self.assertTrue(valid_move(self.board, "V", 0, 0))
        self.board.add_line("V", 0, 0, player=0)
        self.assertTrue(self.board.vertical[0][0])

    def test_invalid_and_repeated_move(self):
        self.assertFalse(valid_move(self.board, "H", 5, 0))
        self.board.add_line("H", 0, 0, player=0)
        self.assertFalse(valid_move(self.board, "H", 0, 0))

    def test_box_completion(self):
        self.board.add_line("H", 0, 0, player=0)
        self.board.add_line("V", 0, 0, player=0)
        self.board.add_line("V", 0, 1, player=0)

        claimed = self.board.add_line("H", 1, 0, player=1)

        self.assertEqual(len(claimed), 1)
        self.assertEqual(self.board.completed[(0, 0)], 1)

    def test_end_of_game_condition(self):
        self.assertFalse(self.board.is_complete())

        for r in range(3):
            for c in range(2):
                self.board.add_line("H", r, c, player=0)

        for r in range(2):
            for c in range(3):
                self.board.add_line("V", r, c, player=0)

        self.assertTrue(self.board.is_complete())

    def test_parse_move_input_sanitization(self):
        self.assertEqual(parse_move("h 0 1"), ("H", 0, 1))
        self.assertIsNone(parse_move("X 0 1"))
        self.assertIsNone(parse_move("H A B"))
        self.assertIsNone(parse_move("H 0"))


if __name__ == "__main__":
    unittest.main()
from board import Board
from rules import valid_move, parse_move


class DotsAndBoxes:
    def __init__(self, rows=2, cols=2):
        print("=== Welcome to Dots and Boxes ===")
        print("Set board grid dimensions (default: 2x2)")

        try:
            r_in = input("Enter rows (default 2): ").strip()
            c_in = input("Enter columns (default 2): ").strip()

            rows = int(r_in) if r_in else 2
            cols = int(c_in) if c_in else 2

            if rows < 1 or cols < 1:
                print("Invalid dimensions. Defaulting to 2x2.")
                rows, cols = 2, 2

        except ValueError:
            print("Invalid input. Defaulting to 2x2.")
            rows, cols = 2, 2

        self.board = Board(rows=rows, cols=cols)
        self.current = 0
        self.scores = [0, 0]

    def run(self):
        print("\nEnter moves as 'H row col' or 'V row col'.")
        print("Rows and columns start at 0.")
        print("Example: H 0 0\n")

        while not self.board.is_complete():
            self.board.display(self.scores, self.current)

            raw = input(
                f"Player {self.current + 1}, enter move: "
            )

            parsed = parse_move(raw)

            if not parsed:
                print(
                    "--> Invalid format or non-integer input! "
                    "Use format: H 0 1"
                )
                continue

            orientation, row, col = parsed

            if not valid_move(
                self.board,
                orientation,
                row,
                col
            ):
                print(
                    "--> Move invalid, out of bounds, "
                    "or edge already filled."
                )
                continue

            newly_claimed = self.board.add_line(
                orientation,
                row,
                col,
                self.current
            )

            if newly_claimed:
                count = len(newly_claimed)

                self.scores[self.current] += count

                print(
                    f"--> Success! Player {self.current + 1} "
                    f"completed {count} box(es) "
                    f"and earns another turn!"
                )
            else:
                self.current = 1 - self.current

        self.board.display(self.scores, self.current)

        print("=== GAME OVER ===")

        if self.scores[0] == self.scores[1]:
            print("Result: The game is a draw!")
        else:
            winner = 1 if self.scores[0] > self.scores[1] else 2

            print(
                f"Result: Player {winner} wins "
                f"with {self.scores[winner - 1]} points!"
            )
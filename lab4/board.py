class Board:
    def __init__(self, rows=2, cols=2):
        self.rows = rows
        self.cols = cols
        self.horizontal = [[False] * cols for _ in range(rows + 1)]
        self.vertical = [[False] * (cols + 1) for _ in range(rows)]
        self.completed = {}

    def add_line(self, orientation, row, col, player):
        if orientation == "H":
            self.horizontal[row][col] = True
        else:
            self.vertical[row][col] = True
        return self._update_completed(player)

    def _update_completed(self, player):
        newly_claimed = []
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.completed:
                    if (
                        self.horizontal[r][c]
                        and self.horizontal[r + 1][c]
                        and self.vertical[r][c]
                        and self.vertical[r][c + 1]
                    ):
                        self.completed[(r, c)] = player
                        newly_claimed.append((r, c))
        return newly_claimed

    def is_complete(self):
        total = self.rows * (self.cols + 1) + self.cols * (self.rows + 1)
        used = sum(map(sum, self.horizontal)) + sum(map(sum, self.vertical))
        return used == total

    def display(self, scores, current):
        print()
        print(f"Scores: Player 1 = {scores[0]} | Player 2 = {scores[1]}  --->  Current Turn: Player {current + 1}")

        for r in range(self.rows + 1):
            line = "."
            for c in range(self.cols):
                line += "---" if self.horizontal[r][c] else "   "
                line += "."
            print(line)

            if r < self.rows:
                middle = []
                for c in range(self.cols + 1):
                    wall = "|" if self.vertical[r][c] else " "
                    middle.append(wall)
                    if c < self.cols:
                        owner = self.completed.get((r, c))
                        label = f"P{owner + 1}" if owner is not None else "  "
                        middle.append(f" {label} ")
                print("".join(middle))
        print()
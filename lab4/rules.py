def valid_move(board, orientation, row, col):
    if orientation not in {"H", "V"}:
        return False

    if orientation == "H":
        return (
            0 <= row <= board.rows
            and 0 <= col < board.cols
            and not board.horizontal[row][col]
        )

    return (
        0 <= row < board.rows
        and 0 <= col <= board.cols
        and not board.vertical[row][col]
    )


def parse_move(raw_input):
    parts = raw_input.strip().upper().split()

    if len(parts) != 3:
        return None

    orientation, r_str, c_str = parts

    if orientation not in {"H", "V"}:
        return None

    try:
        row = int(r_str)
        col = int(c_str)
        return orientation, row, col
    except ValueError:
        return None
import chess


def load_board(fen_or_startpos: str = "startpos") -> chess.Board:
    if fen_or_startpos == "startpos":
        return chess.Board()
    return chess.Board(fen_or_startpos)


def validate_move(board: chess.Board, move: chess.Move) -> tuple[bool, str | None]:
    if move not in board.legal_moves:
        return False, "Illegal move for current position."

    return True, None


def build_payload(board: chess.Board, uci: str, san: str) -> dict:
    return {
        "type": "move.made",
        "fen": board.fen(),
        "uci": uci,
        "san": san,
        "turn": "white" if board.turn else "black",
        "is_check": board.is_check(),
        "is_game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None,
    }

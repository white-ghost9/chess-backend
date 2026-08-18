import chess
from django.db import transaction
from django.utils import timezone
from .models import Match, RatingHistory


class GameManager:
    def __init__(self, match: Match):
        self.match = match
        self.board = self._build_board(match.current_fen)

    def _build_board(self, fen: str):
        if fen in ("startpos", chess.STARTING_FEN):
            return chess.Board()
        return chess.Board(fen)

    def apply_move(self, user, move_data):
        if self.match.status not in {"active", "pending"}:
            return {"valid": False, "reason": "Match is not active"}

        if self.match.status == "pending":
            self.match.status = "active"
            if not self.match.started_at:
                self.match.started_at = timezone.now()
            self.match.save(update_fields=["status", "started_at"])

        player_color = self._player_color(user)
        if player_color != self.match.turn:
            return {"valid": False, "reason": "Not your turn"}

        try:
            move = chess.Move.from_uci(move_data["uci"])
        except Exception:
            return {"valid": False, "reason": "Invalid move format"}

        if move not in self.board.legal_moves:
            return {"valid": False, "reason": "Illegal move"}

        with transaction.atomic():
            self.match = Match.objects.select_for_update().get(pk=self.match.id)
            self.board = self._build_board(self.match.current_fen)
            san = self.board.san(move)
            self.board.push(move)
            self.match.move_history.append(
                {
                    "uci": move.uci(),
                    "san": san,
                    "fen": self.board.fen(),
                }
            )
            self.match.current_fen = self.board.fen()
            self.match.turn = "white" if self.board.turn else "black"

            if self.board.is_game_over():
                self._finalize_game()

            self.match.save()

        payload = {
            "match_id": self.match.id,
            "uci": move.uci(),
            "san": san,
            "fen": self.match.current_fen,
            "turn": self.match.turn,
            "move_history": self.match.move_history,
            "status": self.match.status,
            "result": self.match.result,
        }

        return {"valid": True, "payload": payload}

    def _finalize_game(self):
        self.match.status = "finished"
        self.match.finished_at = timezone.now()
        if self.board.is_checkmate():
            winner = (
                self.match.white_player
                if self.board.turn == chess.BLACK
                else self.match.black_player
            )
            self.match.result = (
                "white_win" if winner == self.match.white_player else "black_win"
            )
            self.match.winner = winner
        elif (
            self.board.is_stalemate()
            or self.board.is_insufficient_material()
            or self.board.can_claim_draw()
        ):
            self.match.result = "draw"
            self.match.winner = None
        else:
            self.match.result = "aborted"
            self.match.winner = None

    def _player_color(self, user):
        if user.id == self.match.white_player_id:
            return "white"
        if user.id == self.match.black_player_id:
            return "black"
        return None

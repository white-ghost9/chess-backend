import json
import chess
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Match, User
from .game_logic import GameManager

ROOM_STATES = {}


class MatchConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"].get("room_name", "default")
        self.room_group_name = f"match_{self.room_name}"

        user = self.scope["user"]
        if user.is_authenticated:
            self.user = user
        else:
            self.user = await self._create_guest_user()

        self.user.status = "online"
        await database_sync_to_async(self.user.save)()

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        state = ROOM_STATES.setdefault(
            self.room_name, {"board": chess.Board(), "turn": "w"}
        )
        await self.send_json(
            {
                "type": "match.joined",
                "room_name": self.room_name,
                "fen": state["board"].fen(),
                "turn": "white" if state["turn"] == "w" else "black",
            }
        )

    async def receive_json(self, content):
        event_type = content.get("type")
        if event_type == "join.match":
            await self.join_match(content)
        elif event_type == "move.make":
            await self.handle_move(content)
        elif event_type == "match.sync":
            await self.sync_match(content)

    async def join_match(self, content):
        room_name = content.get("room_name") or self.room_name
        state = ROOM_STATES.setdefault(room_name, {"board": chess.Board(), "turn": "w"})
        await self.send_json(
            {
                "type": "match.joined",
                "room_name": room_name,
                "fen": state["board"].fen(),
                "turn": "white" if state["turn"] == "w" else "black",
            }
        )

    async def handle_move(self, content):
        room_name = content.get("room_name") or self.room_name
        state = ROOM_STATES.setdefault(room_name, {"board": chess.Board(), "turn": "w"})
        board = state["board"]
        move_uci = content.get("move", {}).get("uci")
        if not move_uci:
            await self.send_json({"type": "error", "message": "Missing move UCI."})
            return

        try:
            move = chess.Move.from_uci(move_uci)
        except ValueError:
            await self.send_json(
                {"type": "move.invalid", "reason": "Invalid move format"}
            )
            return

        if move not in board.legal_moves:
            await self.send_json(
                {"type": "move.invalid", "reason": "Illegal move for current position"}
            )
            return

        san = board.san(move)
        board.push(move)
        state["turn"] = "b" if board.turn else "w"

        payload = {
            "type": "move.made",
            "room_name": room_name,
            "fen": board.fen(),
            "uci": move_uci,
            "san": san,
            "turn": "white" if state["turn"] == "w" else "black",
            "is_check": board.is_check(),
            "is_game_over": board.is_game_over(),
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_move",
                "payload": payload,
            },
        )

    async def broadcast_move(self, event):
        await self.send_json(event["payload"])

    async def sync_match(self, content):
        room_name = content.get("room_name") or self.room_name
        state = ROOM_STATES.setdefault(room_name, {"board": chess.Board(), "turn": "w"})
        await self.send_json(
            {
                "type": "match.state",
                "room_name": room_name,
                "fen": state["board"].fen(),
                "turn": "white" if state["turn"] == "w" else "black",
                "status": "active",
            }
        )

    async def get_match(self, match_id):
        if match_id is None:
            return None
        try:
            return await Match.objects.aget(id=match_id)
        except Match.DoesNotExist:
            return None

    @database_sync_to_async
    def _create_guest_user(self):
        user, _ = User.objects.get_or_create(
            username="guest",
            defaults={"email": "guest@example.com"},
        )
        if not user.has_usable_password():
            user.set_password("guest")
            user.save(update_fields=["password"])
        return user

    async def disconnect(self, code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

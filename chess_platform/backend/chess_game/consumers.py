import json
import chess
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room
from .utils import load_board, build_payload, validate_move


class ChessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chess_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        room = await self.get_room()
        board = load_board(room.fen)
        await self.send(
            text_data=json.dumps(
                {
                    "type": "game.state",
                    "fen": board.fen(),
                    "turn": "white" if board.turn else "black",
                }
            )
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return

        data = json.loads(text_data)
        if data.get("type") != "move.make":
            return

        uci = data.get("move", {}).get("uci")
        if not uci:
            await self.send(
                text_data=json.dumps({"type": "error", "message": "Missing move UCI."})
            )
            return

        room = await self.get_room()
        board = load_board(room.fen)
        try:
            move = chess.Move.from_uci(uci)
        except ValueError:
            await self.send(
                text_data=json.dumps(
                    {"type": "move.invalid", "reason": "Invalid move format."}
                )
            )
            return

        valid, reason = validate_move(board, move)
        if not valid:
            await self.send(
                text_data=json.dumps({"type": "move.invalid", "reason": reason})
            )
            return

        san = board.san(move)
        board.push(move)
        room.fen = board.fen()
        await self.save_room(room)

        payload = build_payload(board, uci, san)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_move",
                "payload": payload,
            },
        )

    async def broadcast_move(self, event):
        await self.send(text_data=json.dumps(event["payload"]))

    @database_sync_to_async
    def get_room(self):
        return Room.objects.get_or_create(name=self.room_name)[0]

    @database_sync_to_async
    def save_room(self, room):
        room.save(update_fields=["fen", "updated_at"])

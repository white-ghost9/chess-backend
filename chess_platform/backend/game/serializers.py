from rest_framework import serializers
from .models import User, Match, RatingHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "display_name",
            "rating",
            "status",
            "profile_image_url",
            "bio",
        ]


class MatchSerializer(serializers.ModelSerializer):
    white_player = UserSerializer(read_only=True)
    black_player = UserSerializer(read_only=True)
    winner = UserSerializer(read_only=True)

    class Meta:
        model = Match
        read_only_fields = [
            "current_fen",
            "turn",
            "move_history",
            "winner",
            "status",
            "result",
            "started_at",
            "finished_at",
        ]
        fields = [
            "id",
            "white_player",
            "black_player",
            "status",
            "result",
            "time_control",
            "initial_time_seconds",
            "increment_seconds",
            "started_at",
            "finished_at",
            "move_history",
            "current_fen",
            "turn",
            "winner",
            "match_type",
        ]


class RatingHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    match_id = serializers.IntegerField(source="match.id", read_only=True)

    class Meta:
        model = RatingHistory
        fields = [
            "id",
            "user",
            "match_id",
            "rating_type",
            "old_rating",
            "new_rating",
            "rating_change",
            "created_at",
        ]

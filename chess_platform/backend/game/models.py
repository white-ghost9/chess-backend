import chess
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    display_name = models.CharField(max_length=150, blank=True)
    rating = models.IntegerField(default=1200)
    status = models.CharField(max_length=20, default="offline")
    profile_image_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Match(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("finished", "Finished"),
    ]
    RESULT_CHOICES = [
        ("white_win", "White Win"),
        ("black_win", "Black Win"),
        ("draw", "Draw"),
        ("resigned", "Resigned"),
        ("timeout", "Timeout"),
        ("aborted", "Aborted"),
    ]

    white_player = models.ForeignKey(
        User, related_name="white_matches", on_delete=models.CASCADE
    )
    black_player = models.ForeignKey(
        User, related_name="black_matches", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    result = models.CharField(
        max_length=20, choices=RESULT_CHOICES, blank=True, null=True
    )
    time_control = models.CharField(max_length=20, default="5+0")
    initial_time_seconds = models.IntegerField(default=300)
    increment_seconds = models.IntegerField(default=0)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    move_history = models.JSONField(default=list, blank=True)
    current_fen = models.CharField(max_length=100, default=chess.STARTING_FEN)
    turn = models.CharField(max_length=5, default="white")
    winner = models.ForeignKey(
        User,
        related_name="won_matches",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    match_type = models.CharField(max_length=20, default="rated")

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["match_type"]),
            models.Index(fields=["white_player"]),
            models.Index(fields=["black_player"]),
            models.Index(fields=["winner"]),
        ]

    def __str__(self):
        return f"Match {self.id}: {self.white_player} vs {self.black_player}"


class RatingHistory(models.Model):
    RATING_TYPE_CHOICES = [
        ("bullet", "Bullet"),
        ("blitz", "Blitz"),
        ("rapid", "Rapid"),
    ]

    user = models.ForeignKey(
        User, related_name="rating_history", on_delete=models.CASCADE
    )
    match = models.ForeignKey(
        Match, related_name="rating_history", on_delete=models.CASCADE
    )
    rating_type = models.CharField(
        max_length=20, choices=RATING_TYPE_CHOICES, default="blitz"
    )
    old_rating = models.IntegerField()
    new_rating = models.IntegerField()
    rating_change = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating change for {self.user} in match {self.match.id}: {self.rating_change}"

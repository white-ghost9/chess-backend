from django.contrib import admin
from .models import User, Match, RatingHistory


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "rating", "status", "last_login"]
    search_fields = ["username", "email"]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "white_player",
        "black_player",
        "status",
        "result",
        "time_control",
    ]
    list_filter = ["status", "result", "time_control"]
    search_fields = ["white_player__username", "black_player__username"]


@admin.register(RatingHistory)
class RatingHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "match", "rating_type", "rating_change", "created_at"]
    list_filter = ["rating_type"]
    search_fields = ["user__username", "match__id"]

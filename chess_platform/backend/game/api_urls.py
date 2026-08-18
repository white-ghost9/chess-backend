from django.urls import path
from . import api_views

urlpatterns = [
    path("me/", api_views.CurrentUserView.as_view(), name="api-me"),
    path("matches/", api_views.MatchListView.as_view(), name="api-matches"),
    path(
        "matches/<int:pk>/",
        api_views.MatchDetailView.as_view(),
        name="api-match-detail",
    ),
]

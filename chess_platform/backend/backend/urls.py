from django.contrib import admin
from django.urls import include, path

from game.views import game_view

urlpatterns = [
    path("", game_view, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("game.api_urls")),
]

from django.urls import path
from .views import game_board, create_game, winning, long_polling

urlpatterns = [
    path("game_board/", game_board, name="game_board"),
    path("create_game/", create_game, name="create_game"),
    path("winning", winning, name="winning"),
    path("long_polling", long_polling, name="long_polling")
    # path('player_actions/', player_actions, name='player_actions'),
]

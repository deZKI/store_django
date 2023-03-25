from django.urls import path

from games.views import GameView, GameListView, ModalGameView

app_name = 'games'
urlpatterns = [
    path('', GameListView.as_view(), name='catalog'),
    path('modal-game/<slug:game_slug>', ModalGameView.as_view(), name='modal_game_view'),
    path('game/<slug:game_slug>', GameView.as_view(), name='game'),
]

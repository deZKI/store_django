from django.urls import path

from games.views import GameView, GameListView

app_name = 'games'
urlpatterns = [
    path('', GameListView.as_view(), name='catalog'),
    path('game/<slug:game_slug>', GameView.as_view(), name='game'),
]

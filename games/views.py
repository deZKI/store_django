from django.db.models import Avg
from django.views.generic import DetailView, TemplateView

from common.views import CommonContextMixin
from games.models import Game, GameGenre, Tag, Rating


class IndexView(CommonContextMixin, TemplateView):
    template_name = 'games/index.html'
    title = 'Главная страница'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['random_games'] = Game.objects.order_by("?").only('name', 'slug', 'main_image')[:3]
        context['wishlist'] = Game.objects.annotate(average_rating=Avg('game_score__rating')).filter(average_rating__gt=0).order_by('-average_rating')[:4]
        context['games_recently_released'] = Game.objects.order_by("-id")[:8].annotate(average_rating=Avg('game_score__rating'))
        return context


class GameListView(CommonContextMixin, TemplateView):
    """Получение нефильтрованного(светлого) списка"""
    title = 'Каталог'
    template_name = 'games/catalog.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GameListView, self).get_context_data()
        context['genres'] = GameGenre.objects.all().values('name', 'slug')
        context['tags'] = Tag.objects.all().values('name', 'slug')
        return context


class ModalGameView(DetailView):
    """Класс для ajax получение quickview по игры"""
    template_name = 'games/product-quick-view.html'
    slug_url_kwarg = 'game_slug'
    queryset = Game.objects.select_related('developer', 'publisher'). \
        prefetch_related('images').annotate(average_rating=Avg('game_score__rating'))


class GameView(DetailView):
    """Для отображения информации об определенной игре"""
    template_name = 'games/game.html'
    slug_url_kwarg = 'game_slug'
    queryset = Game.objects.select_related('developer', 'publisher').prefetch_related('images').annotate(average_rating=Avg('game_score__rating'))

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context['title'] = self.object.name
        # context['']
        if self.request.user.is_authenticated:
            context['user_rating'] = Rating.objects.filter(user=self.request.user, game_id=self.object.id).first()
        return context



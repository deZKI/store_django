from django.db.models import Avg, Count
from django.views.generic import DetailView, TemplateView
from django.db.models import Q

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


class GameView(DetailView):
    """Для отображения информации об определенной игре"""
    template_name = 'games/game.html'
    slug_url_kwarg = 'game_slug'
    queryset = Game.objects.select_related('developer', 'publisher').prefetch_related('images').annotate(average_rating=Avg('game_score__rating'))

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context['title'] = self.object.name

        game_id = self.object.id
        genres = self.object.genres.only('slug')
        tags = self.object.tags.only('slug')

        genres_slug = []
        tags_slug = []
        for g in genres:
            genres_slug.append(g.slug)
        for t in tags:
            tags_slug.append(t.slug)
        context['related_games'] = Game.objects.filter(Q(genres__slug__in=genres_slug) | Q(tags__slug__in=tags_slug)).annotate(wish_count=Count('wish_list'),
                                                                  average_rating=Avg('game_score__rating')).exclude(id=game_id).order_by('-wish_count')[:4]

        if self.request.user.is_authenticated:
            context['user_rating'] = Rating.objects.filter(user=self.request.user, game_id=self.object.id).first()
        return context



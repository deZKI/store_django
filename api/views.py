from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


from api.serializers import GameSerializer, BasketSerializer
from api.services import GamePagination, GameFilter
from games.models import Game, BasketItem, Rating


class GameListAPIView(ListAPIView):
    queryset = Game.objects.annotate(average_rating=Avg('game_score__rating'))
    serializer_class = GameSerializer
    pagination_class = GamePagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = GameFilter
    ordering_fields = ['name', 'price', 'release_date', 'average_rating']


# Исправить на сессии? Вопрос: вычисление на уроне бд или в питоне?
class BasketModelViewSet(ModelViewSet):
    queryset = BasketItem.objects.all().prefetch_related('game')
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication]
    pagination_class = None

    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset().filter(user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response_data = {'games': response.data}
        response.data = response_data
        return response


@login_required
def rate(request, game_id, rating):
    if rating > 5:
        rating = 5
    elif rating < 0:
        rating = 0

    Rating.objects.update_or_create(game_id=game_id, user=request.user, defaults={'rating': rating})
    return HttpResponse('')

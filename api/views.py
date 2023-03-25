from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.services import GamePagination, GameFilter
from api.serializers import GameSerializer, BasketSerializer

from games.models import Game, BasketItem, Rating




# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


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
    lookup_field = 'id'

    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset().filter(user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        response_data = {'games': response.data}
        response.data = response_data
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@login_required
def rate(request, game_id, rating):
    Rating.objects.update_or_create(game_id=game_id, user=request.user, defaults={'rating': rating})
    return HttpResponse('')


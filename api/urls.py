from django.urls import path, include
from django.views.decorators.cache import cache_page

from api.views import GameListAPIView, BasketModelViewSet, rate
from rest_framework import routers

router = routers.SimpleRouter()
router.register('baskets', BasketModelViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('game_list/', cache_page(600)(GameListAPIView.as_view()), name='get_games'),
    path('rate/<int:game_id>/<int:rating>/', rate),

    # path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]

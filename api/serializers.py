from rest_framework import serializers

from games.models import Game, BasketItem
from users.models import User


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'slug', 'price', 'main_image', 'average_rating')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class BasketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BasketItem
        fields = ('id', 'game', 'quantity', 'sum', 'created_timestamp')
        read_only_fields = ('created_timestamp',)

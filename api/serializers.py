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

    def create(self, validated_data):
        data = validated_data
        del data['quantity']
        if BasketItem.objects.filter(**data).exists():
            basket = BasketItem.objects.get(**validated_data)
            basket.quantity = basket.quantity + 1
            basket.save()
        else:
            basket=BasketItem.objects.create(**validated_data)
        return basket

    class Meta:
        model = BasketItem
        fields = ('id', 'user', 'game', 'quantity', 'sum', 'created_timestamp')
        read_only_fields = ('created_timestamp',)



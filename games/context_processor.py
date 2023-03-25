from games.models import BasketItem


# 'baskets' стала глобальной

def baskets(request):
    user = request.user
    context = dict()
    if user.is_authenticated:
        context['baskets'] = BasketItem.objects.filter(user=user).prefetch_related('game')
    return context

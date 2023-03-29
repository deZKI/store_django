from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView

from common.views import CommonContextMixin
from .models import MainPage


class IndexView(CommonContextMixin, TemplateView):
    template_name = 'pages/index.html'
    title = 'Главная страница'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['games'] = MainPage.objects.filter(isIndex=True).first().games.annotate(
            average_rating=Avg('game_score__rating')).all()
        context['object'] = MainPage.objects.filter(isIndex=True).first()
        return context


class PageView(DetailView):
    """Для отображения информации об определенной игре"""
    template_name = 'pages/index.html'
    slug_url_kwarg = 'page_slug'
    model = MainPage

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context['title'] = self.object.name
        context['games'] = context['object'].games.annotate(
            average_rating=Avg('game_score__rating')).all()
        return context

    def get(self, request, *args, **kwargs):
        response = super(PageView, self).get(request, *args, **kwargs)
        if request.user.is_active:
            return response
        else:
            return HttpResponseRedirect(reverse('index'))

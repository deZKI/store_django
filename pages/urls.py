from django.urls import path

from .views import PageView, IndexView

app_name = 'pages'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('page/<slug:page_slug>', PageView.as_view(),  name='page'),
]

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from utils.scrapping import parsing
from games.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('test/', include('pages.urls'), name='pages'),

    path('catalog/', include('games.urls', namespace='games')),
    path('users/', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls', namespace='orders')),
    path('api/v1/', include('api.urls', namespace='api')),

    path('dump_games/<int:page>', parsing, name='parsing'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
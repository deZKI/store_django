from django.urls import path

from orders.views import OrderCreateView, SuccessTemplateView, CanceledTemplateView, \
    OrderListView, OrderDetailView, webhook_yookassa

app_name = 'orders'
urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('success/', SuccessTemplateView.as_view(), name='order_success'),
    path('canceled/', CanceledTemplateView.as_view(), name='order_canceled'),

    path('notification_url/', webhook_yookassa),
]

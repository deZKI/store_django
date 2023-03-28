import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView

from yookassa import Configuration, Payment
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory

from common.views import CommonContextMixin
from games.models import BasketItem
from orders.forms import OrderCreateForm
from orders.models import Order

Configuration.configure(secret_key=settings.YOOKASSA_SECRET_KEY, account_id=settings.YOOKASSA_SHOP_ID)


# response = Webhook.add({
#     "event": "payment.succeeded",
#     "url": "https://e621-185-48-112-241.jp.ngrok.io/orders/notification_url/",
# })

class OrderCreateView(LoginRequiredMixin, CommonContextMixin, CreateView):
    title = 'Оформление заказа'
    template_name = 'orders/order-create.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('orders:order_success')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(self, request, *args, **kwargs)
        games = BasketItem.objects.filter(user=self.request.user)
        # payment = Payment.create(
        #     {
        #         "amount": {
        #             "value": games.total_sum(),
        #             "currency": "RUB"
        #         },
        #         "confirmation": {
        #             "type": "redirect",
        #             "return_url": "{}/orders/orders-success/".format(settings.HOST_URL)
        #         },
        #         "capture": True,
        #         "description": f"Заказ №{self.object.id}",
        #         "metadata": {
        #             'orderNumber': '72'
        #         },
        #         "receipt": {
        #             "customer": {
        #                 "full_name": self.object.first_name,
        #                 "phone": self.object.phone,
        #                 "address": self.object.address
        #             },
        #             "items": games.yookassa_games()
        #         }
        #     })
        # # исправить
        # fulfill_order(self.object)
        # confirmation_url = payment.confirmation.confirmation_url
        # return HttpResponseRedirect(confirmation_url)
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


class OrderListView(CommonContextMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = ('-created')

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView, LoginRequiredMixin):
    template_name = 'orders/order.html'
    model = Order

    def get_object(self, queryset=None):
        obj = super(OrderDetailView, self).get_object(queryset)
        if obj.initiator == self.request.user:
            return obj
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Заказ #{self.object.id}'
        return context


class SuccessTemplateView(CommonContextMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Спасибо за заказ!'


class CanceledTemplateView(CommonContextMixin, TemplateView):
    template_name = 'orders/canceled.html'
    title = 'Заказ не удался'


def webhook_yookassa(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')  # Получите IP запроса
    if not SecurityHelper().is_ip_trusted(ip):
        return HttpResponse(status=400)

    # Извлечение JSON объекта из тела запроса
    event_json = json.loads(request.body)
    try:
        # Создание объекта класса уведомлений в зависимости от события
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }

        elif notification_object.event == WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
            some_data = {
                'refundId': response_object.id,
                'refundStatus': response_object.status,
                'paymentId': response_object.payment_id,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.DEAL_CLOSED:
            some_data = {
                'dealId': response_object.id,
                'dealStatus': response_object.status,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.PAYOUT_SUCCEEDED:
            some_data = {
                'payoutId': response_object.id,
                'payoutStatus': response_object.status,
                'dealId': response_object.deal.id,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.PAYOUT_CANCELED:
            some_data = {
                'payoutId': response_object.id,
                'payoutStatus': response_object.status,
                'dealId': response_object.deal.id,
            }
            # Специфичная логика
            # ...
        else:
            # Обработка ошибок
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

        # Специфичная логика
        # ...
        Configuration.configure('XXXXXX', 'test_XXXXXXXX')
        # Получим актуальную информацию о платеже
        payment_info = Payment.find_one(some_data['paymentId'])
        if payment_info:
            payment_status = payment_info.status
            # Специфичная логика
            # ...
        else:
            # Обработка ошибок
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

    except Exception:
        # Обработка ошибок
        return HttpResponse(status=400)  # Сообщаем кассе об ошибке

    return HttpResponse(status=200)  # Сообщаем кассе, что все хорошо
# Create your views here.

#после деплоя нужно вебхук настроить и поменять

# def fulfill_order(order):
#     # order_id = int(session.metadata.order_id)
#     # order = Order.objects.get(id=order_id)
#     order.update_after_payment()

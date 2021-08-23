from django.conf import settings
from django.db import models

from products.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    DELIVERY = 'DLV'
    DONE = 'DN'
    CANCELED = 'CNC'

    STATUSES = (
        (FORMING, 'Заказ формируется'),
        (SENT_TO_PROCEED, 'Заказ отправлен'),
        (DELIVERY, 'Заказ в доставкеп'),
        (DONE, 'Заказ получен'),
        (CANCELED, 'Заказ отменен')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUSES, default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ номер {self.pk}'

    #def get_total_quantity(self):
    #    items = self.orderitems.select_related()
    #    return sum(list(map(lambda x: x.quantity, items)))

    #def get_total_cost(self):
    #    items = self.orderitems.select_related()
    #    return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }

    def delete(self):
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity